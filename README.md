# LLM-Assisted Analytics Metadata on IFC Models

_A Studio 2.5 collaboration with the Canadian National Research Council_

This project explores how building analytics (embodied carbon, operational carbon, energy, and other performance indicators) can be stored in or linked to IFC models, displayed on IFC geometry, and queried through LLM-based natural-language interfaces.

The work will produce a technical paper and a minimal proof of concept.

## Using this repository with Claude

The repository is set up for [Claude Code](https://claude.com/claude-code). Claude reads `CLAUDE.md` and connects to the IFC query server listed in `.mcp.json`, so you can ask questions about the sample building models in plain English.

1. Install Git, the .NET 8 SDK, Node.js, and Claude Code.
2. Clone with submodules. The BIM Open Toolkit is a submodule, and it has submodules of its own, so the fetch must be recursive:

   ```bash
   git clone --recurse-submodules https://github.com/ara3d/nrc-ifc-llm
   ```

   If you already cloned without that flag, run this from the repository root:

   ```bash
   git submodule update --init --recursive
   ```

3. Build the toolkit's query server once:

   ```bash
   node bim-open-toolkit/scripts/build-mcp.mjs
   ```

4. Start Claude Code in the repository root and approve the `bimopen-ifc` server when asked.
5. Ask questions. Some to try:
   - "How many doors are on each storey of poc/data/duplex-enriched.ifc?"
   - "Which walls in the duplex have the highest embodied carbon?"
   - "Summarize section 4 of the paper."
   - "How do I reproduce the proof of concept?"

The carbon values in `poc/` are synthetic, made up for demonstration.

## Technical paper

- [paper/](paper/README.md) — the technical paper (deliverable D3), one Markdown file per section, with a status table showing which results are executed and which are planned.

## Documents

- [Statement of Work](statement-of-work.md) — background, objectives, scope, deliverables, and acceptance criteria for the engagement.
- [Storing Analytics in IFC](storing-analytics-in-ifc.md) — a brainstorm of options for storing analytics data inside IFC, with pros and cons of each.
- [IDS Overview](ids.md) — an introduction to the Information Delivery Specification (IDS), the buildingSMART standard for machine-readable information requirements.
- [IFC Viewers](ifc-viewers.md) — an inventory of open-source IFC viewers.
- [Intro to Git](intro-to-git.md) — a brief introduction to Git and this repository for new contributors.

## Data

The `data/` folder contains sample IFC models used for experimentation:

- `AC20-FZK-Haus.ifc`
- `C20-Institute-Var-2.ifc`
- `duplex.ifc`
- `Office_A_20110811.ifc`
