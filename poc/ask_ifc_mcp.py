"""Drive the BIM Open Toolkit IFC MCP server over HTTP and append every call and its result
to a Markdown transcript, so a question-answering session is recorded exactly as an MCP
client would see it.

Usage (server started from the toolkit root with
`dotnet run --project deps/bim-open-data/src/mcp/BimOpenMcp.Ifc -- --http 8766`):

    python poc/ask_ifc_mcp.py note "Q1: What is the total operational carbon for the building?"
    python poc/ask_ifc_mcp.py call ifc_sql '{"path": "...", "sql": "SELECT ..."}'
    python poc/ask_ifc_mcp.py answer "37,196 kgCO2e per year across 218 elements."

Transcript: poc/results/transcript.md
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPT = ROOT / "poc" / "results" / "transcript.md"
URL = "http://127.0.0.1:8766/mcp"
MAX_RESULT_CHARS = 3000


def call(tool: str, args: dict) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args}}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.load(resp)


def result_text(response: dict) -> str:
    if "error" in response:
        return "ERROR: " + json.dumps(response["error"])
    content = response.get("result", {}).get("content", [])
    texts = [c.get("text", "") for c in content if c.get("type") == "text"]
    text = "\n".join(texts)
    try:
        text = json.dumps(json.loads(text), indent=1)
    except (ValueError, TypeError):
        pass
    return text


def append(block: str) -> None:
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    with open(TRANSCRIPT, "a", encoding="utf-8") as f:
        f.write(block + "\n")


def main() -> None:
    kind = sys.argv[1]
    if kind == "note":
        append(f"\n### {sys.argv[2]}\n")
    elif kind == "answer":
        append(f"**Agent:** {sys.argv[2]}\n")
    elif kind == "call":
        tool, args = sys.argv[2], json.loads(sys.argv[3])
        response = call(tool, args)
        text = result_text(response)
        shown = text if len(text) <= MAX_RESULT_CHARS else text[:MAX_RESULT_CHARS] + f"\n... ({len(text)} chars total)"
        append(f"**Agent calls** `{tool}` with\n```json\n{json.dumps(args, indent=1)}\n```\n"
               f"**Result**\n```json\n{shown}\n```\n")
        print(text)
    else:
        raise SystemExit("usage: ask_ifc_mcp.py note|call|answer ...")


if __name__ == "__main__":
    main()
