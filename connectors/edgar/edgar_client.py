"""SEC EDGAR client: company lookup, filings, XBRL facts and filing text, all with source links.

Free data, no API key. The SEC requires every request to identify a contact in the
User-Agent header, read here from the SEC_USER_AGENT environment variable
(e.g. "Acme Research research@acme.example"). The SEC allows about 10 requests per
second; requests are throttled below that and responses are cached in memory.

The pure functions (classify_period, consolidate_facts, html_to_text, ...) do no network
I/O, so they can be tested offline.
"""
import asyncio
import html
import os
import re
import time
from datetime import date

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accn_nodash}/"
ALLOWED_HOSTS = ("www.sec.gov", "sec.gov", "data.sec.gov")

MIN_INTERVAL_S = 0.15  # stays under the SEC's 10 requests/second
CACHE_TTL_S = 3600


class EdgarError(Exception):
    """An error with a message written for the agent: what went wrong and what to try."""


# ---------- pure helpers (no network) ----------

def classify_period(start, end):
    """Name a fact's period: 'instant', 'quarter', 'annual', or 'ytd-N-months'."""
    if not start:
        return "instant"
    days = (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
    if 80 <= days <= 100:
        return "quarter"
    if 350 <= days <= 380:
        return "annual"
    return f"ytd-{round(days / 30.4)}-months"


def filing_index_url(cik, accn):
    return ARCHIVE_URL.format(cik_int=int(cik), accn_nodash=accn.replace("-", ""))


def consolidate_facts(rows, cik, primary_docs=None):
    """Collapse XBRL rows to one value per period.

    The same period is reported in several filings (each 10-K repeats prior years). Keep
    the most recently filed value, record every filing that reported it, and flag
    `restated` when filings disagree. Note: an XBRL row's `fy` is the *filing's* fiscal
    year, not the period's, so periods are keyed by their start and end dates only.
    """
    primary_docs = primary_docs or {}
    by_period = {}
    for r in rows:
        by_period.setdefault((r.get("start"), r["end"]), []).append(r)

    out = []
    for (start, end), group in by_period.items():
        group.sort(key=lambda r: r["filed"])
        latest = group[-1]
        values = {r["val"] for r in group}
        doc = primary_docs.get(latest["accn"])
        index_url = filing_index_url(cik, latest["accn"])
        out.append({
            "period_start": start,
            "period_end": end,
            "period_type": classify_period(start, end),
            "value": latest["val"],
            "form": latest["form"],
            "filed": latest["filed"],
            "accession": latest["accn"],
            "source_url": index_url + doc if doc else index_url,
            "reported_in_filings": len(group),
            "restated": len(values) > 1,
            "earlier_values": sorted(values - {latest["val"]}) if len(values) > 1 else [],
        })
    out.sort(key=lambda f: (f["period_end"], f["period_start"] or ""))
    return out


def html_to_text(raw):
    """Crude HTML-to-text for filings: drop scripts, styles and tags; collapse whitespace."""
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<ix:header>.*?</ix:header>", " ", raw)  # hidden inline-XBRL block
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h\d)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html.unescape(raw).replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def keyword_snippets(text, keywords, context_chars=400, max_hits=8):
    """Return passages around each keyword hit (case-insensitive), without overlaps."""
    hits = []
    lower = text.lower()
    for kw in keywords:
        start = 0
        while len(hits) < max_hits:
            i = lower.find(kw.lower(), start)
            if i < 0:
                break
            a, b = max(0, i - context_chars), min(len(text), i + len(kw) + context_chars)
            if not any(a < h["end"] and b > h["start"] for h in hits):
                hits.append({"keyword": kw, "start": a, "end": b, "text": text[a:b].strip()})
            start = i + len(kw)
    return sorted(hits, key=lambda h: h["start"])


def check_sec_url(url):
    m = re.match(r"^https://([^/]+)/", url)
    if not m or m.group(1) not in ALLOWED_HOSTS:
        raise EdgarError(f"Only sec.gov URLs can be read, got {url!r}. Use a source_url from "
                         "edgar_list_filings or edgar_get_fact.")


# ---------- network client ----------

class EdgarClient:
    def __init__(self, user_agent=None):
        self.user_agent = user_agent or os.environ.get("SEC_USER_AGENT", "").strip()
        self._cache = {}
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def _get(self, url, as_json=True):
        if not self.user_agent:
            raise EdgarError("SEC_USER_AGENT is not set. The SEC requires a contact in the "
                             "User-Agent, e.g. 'Firm Name contact@firm.example'. Ask the user "
                             "to set it; do not invent one.")
        hit = self._cache.get(url)
        if hit and time.monotonic() - hit[0] < CACHE_TTL_S:
            return hit[1]
        async with self._lock:
            wait = MIN_INTERVAL_S - (time.monotonic() - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            import httpx  # imported here so the pure helpers work without it

            async with httpx.AsyncClient(timeout=30, follow_redirects=True,
                                         headers={"User-Agent": self.user_agent}) as http:
                resp = await http.get(url)
            self._last = time.monotonic()
        if resp.status_code == 404:
            raise EdgarError(f"Not found on EDGAR: {url}")
        if resp.status_code in (403, 429):
            raise EdgarError(f"EDGAR refused the request ({resp.status_code}). Wait a minute "
                             "and retry; check SEC_USER_AGENT is a real contact.")
        resp.raise_for_status()
        data = resp.json() if as_json else resp.text
        self._cache[url] = (time.monotonic(), data)
        return data

    async def find_company(self, ticker):
        tickers = await self._get(TICKERS_URL)
        t = ticker.strip().upper()
        for row in tickers.values():
            if row["ticker"].upper() == t:
                cik = f"{int(row['cik_str']):010d}"
                sub = await self._get(SUBMISSIONS_URL.format(cik=cik))
                return {"ticker": t, "cik": cik, "name": sub["name"],
                        "fiscal_year_end_mmdd": sub.get("fiscalYearEnd"),
                        "sic_description": sub.get("sicDescription")}
        raise EdgarError(f"Ticker {ticker!r} not found in the SEC ticker list.")

    async def _submissions(self, ticker):
        company = await self.find_company(ticker)
        return company, await self._get(SUBMISSIONS_URL.format(cik=company["cik"]))

    async def list_filings(self, ticker, forms, limit):
        company, sub = await self._submissions(ticker)
        r = sub["filings"]["recent"]
        wanted = {f.upper() for f in forms}
        out = []
        for i, form in enumerate(r["form"]):
            if wanted and form.upper() not in wanted:
                continue
            accn = r["accessionNumber"][i]
            out.append({"form": form, "filed": r["filingDate"][i], "period": r["reportDate"][i],
                        "accession": accn, "description": r["primaryDocDescription"][i],
                        "source_url": filing_index_url(company["cik"], accn) + r["primaryDocument"][i],
                        "index_url": filing_index_url(company["cik"], accn)})
            if len(out) >= limit:
                break
        return company, out

    async def _facts(self, ticker):
        company, sub = await self._submissions(ticker)
        facts = await self._get(FACTS_URL.format(cik=company["cik"]))
        r = sub["filings"]["recent"]
        docs = dict(zip(r["accessionNumber"], r["primaryDocument"]))
        return company, facts, docs

    async def search_concepts(self, ticker, keyword, limit):
        company, facts, _ = await self._facts(ticker)
        kw = keyword.lower()
        out = []
        for taxonomy, concepts in facts["facts"].items():
            for name, c in concepts.items():
                label = c.get("label") or ""
                if kw in name.lower() or kw in label.lower():
                    rows = [r for rows in c["units"].values() for r in rows]
                    out.append({"concept": f"{taxonomy}:{name}", "label": label,
                                "units": list(c["units"]),
                                "latest_period_end": max(r["end"] for r in rows) if rows else None})
        out.sort(key=lambda c: c["latest_period_end"] or "", reverse=True)
        return company, out[:limit]

    async def get_fact(self, ticker, concept, period_type, limit):
        company, facts, docs = await self._facts(ticker)
        taxonomy, _, name = concept.rpartition(":")
        taxonomy = taxonomy or "us-gaap"
        c = facts["facts"].get(taxonomy, {}).get(name)
        if c is None:
            raise EdgarError(f"{taxonomy}:{name} is not reported by {company['name']}. Use "
                             "edgar_search_concepts to find the tag this company uses.")
        result = {"company": company, "concept": f"{taxonomy}:{name}",
                  "label": c.get("label"), "description": c.get("description"), "units": {}}
        for unit, rows in c["units"].items():
            vals = consolidate_facts(rows, company["cik"], docs)
            if period_type != "all":
                vals = [v for v in vals if v["period_type"] == period_type]
            result["units"][unit] = vals[-limit:]
        return result

    async def read_filing(self, url, keywords, max_chars):
        check_sec_url(url)
        text = html_to_text(await self._get(url, as_json=False))
        if keywords:
            return {"source_url": url, "length": len(text),
                    "snippets": keyword_snippets(text, keywords)}
        return {"source_url": url, "length": len(text), "text": text[:max_chars],
                "truncated": len(text) > max_chars}
