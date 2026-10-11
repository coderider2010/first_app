#!/usr/bin/env bash
# Launch the EDGAR MCP server over stdio, creating the project virtualenv on first use.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="$ROOT/.venv"
if [ ! -x "$VENV/bin/python" ] || ! "$VENV/bin/python" -c "import mcp, httpx" 2>/dev/null; then
  python3 -m venv "$VENV" >&2
  "$VENV/bin/pip" install -q -r "$ROOT/connectors/edgar/requirements.txt" >&2
fi
exec "$VENV/bin/python" "$ROOT/connectors/edgar/server.py"
