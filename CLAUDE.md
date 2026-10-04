# Working in this repository

This repository holds a technical paper and a proof of concept on storing building analytics in IFC models and querying them in natural language. The BIM Open Toolkit is a git submodule at `bim-open-toolkit/`; its code is not edited from here.

The submodule is pinned to a tagged tested set of the toolkit (`v0.1`). The toolkit takes its own dependencies (the BIM Open data, flow, viewer, notebook, and schema repositories, Gratify, and the Ara 3D SDK and dataflow engine) from `bim-open-toolkit/deps/`, filled by `node deps.mjs` from `bim-open-toolkit/deps.json`. If `bim-open-toolkit/` is empty, run `git submodule update --init` from this repository's root; if `bim-open-toolkit/deps/` is empty, run `node deps.mjs` inside `bim-open-toolkit/`. Nothing builds until both have been done.

- Before answering a question about an `.ifc` file, read `bim-open-toolkit/.claude/skills/ifc-ask/SKILL.md` and the `ifc-guide.md` beside it. The `bimopen-ifc` MCP server in `.mcp.json` answers those questions. Pass absolute paths with forward slashes.
- If the `bimopen-ifc` server is missing, it has not been built: run `node scripts/build-mcp.mjs` inside `bim-open-toolkit/`, then ask the user to restart Claude Code.
- Sample models: `data/`, `IFC-Test-Kit/`, and `poc/data/duplex-enriched.ifc` (duplex with synthetic carbon property sets).
- The paper is in `paper/` (start at `paper/README.md`); the proof of concept and how to reproduce it are in `poc/README.md`.
- Analytics values in `poc/` are synthetic. Say so when quoting them.

## Checks

- `REQUIREMENTS.md` is the requirements table; update a row's status and check when work changes it.
- CI is `.github/workflows/check.yml`; the README's "Checks" section has the local commands.
- After editing documentation that names a toolkit path, run `python checks/check_toolkit_paths.py`. A path the pinned toolkit lacks fails it; list a deliberate exception in `checks/known-missing-paths.txt` with the reason.
- After changing `poc/data/` or `poc/expected_answers.py`, run `python poc/check_answers.py`.
