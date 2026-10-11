#!/usr/bin/env python3
"""edgar_mcp: an MCP server that gives agents source-linked SEC EDGAR data.

Every value it returns carries the filing it came from (form, filing date, accession and
a sec.gov link), so the Associate can satisfy "every number has a lineage".

Run (stdio):  SEC_USER_AGENT="Firm contact@firm.example" python connectors/edgar/server.py
"""
import sys
from pathlib import Path
from typing import Annotated, Literal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edgar_client import EdgarClient, EdgarError  # noqa: E402

mcp = MCPServer(
    "edgar_mcp",
    instructions=(
        "Free SEC EDGAR data. Typical flow: edgar_list_filings to find the latest 10-K/10-Q; "
        "edgar_search_concepts to find the XBRL tag a company uses; edgar_get_fact for the "
        "values (one per period, latest filing wins, restatements flagged); edgar_read_filing "
        "for figures that are only in the text, such as customer counts. Cite source_url "
        "for every number."
    ),
)
client = EdgarClient()
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True,
                            openWorldHint=True)


async def _agent_errors(coro):
    """Re-raise EdgarError as ToolError so its guidance reaches the agent, not just the log."""
    try:
        return await coro
    except EdgarError as e:
        raise ToolError(str(e)) from e


Ticker = Annotated[str, Field(description="Stock ticker, e.g. 'HUBS'", min_length=1, max_length=10)]


@mcp.tool(name="edgar_find_company", annotations=READ_ONLY)
async def edgar_find_company(ticker: Ticker) -> dict:
    """Look up a company by ticker: SEC CIK number, legal name, fiscal year end (MMDD), industry."""
    return await _agent_errors(client.find_company(ticker))


@mcp.tool(name="edgar_list_filings", annotations=READ_ONLY)
async def edgar_list_filings(
    ticker: Ticker,
    forms: Annotated[list[str], Field(description="Form types to include, e.g. ['10-K','10-Q','8-K']. Empty = all.")] = ["10-K", "10-Q"],
    limit: Annotated[int, Field(ge=1, le=50, description="Maximum filings, newest first")] = 10,
) -> dict:
    """List a company's recent filings, newest first, each with its period, filing date and a link to the document."""
    company, filings = await _agent_errors(client.list_filings(ticker, forms, limit))
    return {"company": company, "filings": filings}


@mcp.tool(name="edgar_search_concepts", annotations=READ_ONLY)
async def edgar_search_concepts(
    ticker: Ticker,
    keyword: Annotated[str, Field(min_length=2, description="Word to match in XBRL tag names or labels, e.g. 'revenue', 'StockBased', 'shares'")],
    limit: Annotated[int, Field(ge=1, le=100)] = 25,
) -> dict:
    """Find which XBRL tags (concepts) a company reports, by keyword. Companies tag the same idea differently, so search before calling edgar_get_fact."""
    company, concepts = await _agent_errors(client.search_concepts(ticker, keyword, limit))
    return {"company": company, "concepts": concepts}


@mcp.tool(name="edgar_get_fact", annotations=READ_ONLY)
async def edgar_get_fact(
    ticker: Ticker,
    concept: Annotated[str, Field(description="XBRL concept, e.g. 'us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax' or 'dei:EntityCommonStockSharesOutstanding'")],
    period_type: Annotated[Literal["annual", "quarter", "instant", "all"], Field(description="'annual' or 'quarter' for flows (revenue, cash flow); 'instant' for balances (cash, debt, shares); 'all' includes year-to-date periods")] = "annual",
    limit: Annotated[int, Field(ge=1, le=40, description="Most recent N periods")] = 5,
) -> dict:
    """Get reported values for one XBRL concept: one value per period, from the latest filing that reported it, with a source link. 'restated' is true when filings disagree."""
    return await _agent_errors(client.get_fact(ticker, concept, period_type, limit))


@mcp.tool(name="edgar_read_filing", annotations=READ_ONLY)
async def edgar_read_filing(
    url: Annotated[str, Field(description="A sec.gov document URL, e.g. a source_url from edgar_list_filings")],
    keywords: Annotated[list[str], Field(description="If given, return only passages around these words, e.g. ['customers', 'net revenue retention']")] = [],
    max_chars: Annotated[int, Field(ge=1000, le=100000)] = 20000,
) -> dict:
    """Read a filing as plain text. Use keywords to pull passages for figures not in XBRL (customer counts, retention, guidance)."""
    return await _agent_errors(client.read_filing(url, keywords, max_chars))


if __name__ == "__main__":
    mcp.run("stdio")
