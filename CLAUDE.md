# Working in this repository

This repository holds a technical paper and a proof of concept on storing building analytics in IFC models and querying them in natural language. The BIM Open Toolkit is a git submodule at `bim-open-toolkit/`; its code is not edited from here.

The toolkit has submodules of its own (`bim-open-toolkit/submodules/gratify` and `parakeet`), so submodules must be fetched recursively. If `bim-open-toolkit/` or anything under `bim-open-toolkit/submodules/` is empty, run `git submodule update --init --recursive` from this repository's root before building or answering anything. Plain `git submodule update --init` leaves the nested ones empty and the toolkit will not build.

- Before answering a question about an `.ifc` file, read `bim-open-toolkit/.claude/skills/ifc-ask/SKILL.md` and the `ifc-guide.md` beside it. The `bimopen-ifc` MCP server in `.mcp.json` answers those questions. Pass absolute paths with forward slashes.
- If the `bimopen-ifc` server is missing, it has not been built: run `node scripts/build-mcp.mjs` inside `bim-open-toolkit/`, then ask the user to restart Claude Code.
- Sample models: `data/`, `IFC-Test-Kit/`, and `poc/data/duplex-enriched.ifc` (duplex with synthetic carbon property sets).
- The paper is in `paper/` (start at `paper/README.md`); the proof of concept and how to reproduce it are in `poc/README.md`.
- Analytics values in `poc/` are synthetic. Say so when quoting them.
