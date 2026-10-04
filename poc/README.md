# Proof of concept: synthetic analytics on duplex.ifc

This folder holds the executed proof of concept behind the paper's Section 6.2: a synthetic
analytics dataset, the enriched IFC model written with the BIM Open Toolkit's byte-exact
writer, a recorded question-answering session over that model through the toolkit's IFC MCP
server, and the dataflow graphs used for the screenshots in Section 4. Everything here is
reproducible from the scripts; nothing in `results/` was hand-edited except where the
transcript says so.

The analytics values are **synthetic and illustrative**. They have the shape the paper
recommends (Appendix A) but were generated from per-type base values with a hash jitter, not
from an analysis tool.

## Files

| Path | What it is |
|---|---|
| `generate_synthetic_analytics.py` | Builds the dataset from `IFC-Test-Kit/duplex.ifc` and the test-kit CSV. Deterministic. |
| `data/nrc_analytics_elements.csv` | Layer 1 values, one row per physical element (218 rows). |
| `data/nrc_analytics_long.csv` | Layer 2 table, one row per (run, element, metric). |
| `data/nrc_analytics_storeys.csv` | Storey and building aggregates. |
| `data/psets_to_write.csv` | Rows for the writer: entity id, set name, property, IFC value type, value. |
| `data/duplex-enriched.ifc` | `duplex.ifc` plus 664 property sets, written byte-exactly. |
| `data/view_values.csv`, `data/door_verdicts_w1.csv` | Value tables joined to geometry for the 3D colourings. |
| `EnrichIfc/` | .NET console program: writes the sets with `Ara3D.Ifc.Editing`, diffs, reverses, and hashes. |
| `results/enrich-report.json` | Output of `EnrichIfc`: counts, SHA-256 of source and target, verification flags. |
| `expected_answers.py`, `results/expected_answers.json` | Expected answer per question, computed from the CSV alone. |
| `ask_ifc_mcp.py`, `results/transcript.md` | MCP client helper and the recorded question-answering session. |
| `graphs/*.json` | BimOpenFlow graphs: colour by carbon, by category, by door verdict, and a storey chart. |
| `store/` | The host's analysis store used for the screenshots (graphs plus seeded samples). |

## Reproducing

The toolkit is a git submodule at `bim-open-toolkit/`, pinned to its tagged tested set `v0.1`. After cloning this repository, run `git submodule update --init`, then `node deps.mjs` inside `bim-open-toolkit/` to fetch the repositories the toolkit is built from (the byte-exact writer and the IFC MCP server live in `deps/bim-open-data`).

```bash
python poc/generate_synthetic_analytics.py
```

```bash
dotnet run --project poc/EnrichIfc -c Release -- IFC-Test-Kit/duplex.ifc poc/data/psets_to_write.csv poc/data/duplex-enriched.ifc poc/results/enrich-report.json
```

```bash
python poc/expected_answers.py
```

Start the IFC MCP server over HTTP from the toolkit root, then drive it with `ask_ifc_mcp.py`
(see the docstring for the three sub-commands):

```bash
dotnet run --project deps/bim-open-data/src/mcp/BimOpenMcp.Ifc -- --http 8766
```

The 3D screenshots use the toolkit's host in the `bim` profile with `poc/data` as a model
root and `poc/store` as the analysis store, and the web editor's `3d.html` page. The launch
entries are in `.claude/launch.json`.

## What the session showed

- The writer added 3,766 entities to a 38,898-entity file. The entity diff lists exactly those
  additions, removing them restores the source byte for byte, and a second run is
  byte-identical.
- Every question in the paper's list was answered from the enriched file through one read-only
  SQL tool, with values matching the independently computed expectation, including the
  deliberate absence in Q7.
- One question (Q2) needed a second query: the agent's first grouping used the room, not the
  storey, and the transcript keeps both attempts.

## Reproducing the figures with the toolkit's walkthrough

The toolkit carries copies of this folder's data under `samples/nrc` and the graphs as seeded
samples under `samples/nrc-analyses` (with tests that assert the expected numbers). One command
regenerates every figure and both MCP transcripts:

```bash
npm run nrc:walkthrough --prefix bimopenflow/web
```

Its output index is copied here as `results/walkthrough-index.md`; the IFC MCP replay of Q1,
Q5, Q7, and Q8 is `results/transcript-mcp-replay.md`. The unattended language-model run uses
`bimopenmcp-ifc-ask` with `samples/nrc/questions.txt` (the eight questions verbatim) and is
recorded as `results/transcript-unattended.md` and `results/results-unattended.json`.

## Unattended runs with Claude, scored

`results/unattended/<date>/` holds the runs of the eight questions made with the toolkit's
`bimopenmcp-ifc-ask` runner through the Claude Code command line (model and effort in each
transcript's header), one fresh conversation per question, every tool call recorded. Files named
`new-run<n>` ran over the toolkit's regenerated `samples/nrc/duplex-enriched.ifc` (summary sets
under their own names, version 2 of the paper); files named `old-run<n>` ran over this folder's
`data/duplex-enriched.ifc` (version 1, aggregates under the element names) as a control.

```bash
dotnet run --project bim-open-toolkit/src/studio/BimOpenMcp.Ifc.Ask -c Release -- --model bim-open-toolkit/samples/nrc/duplex-enriched.ifc --questions bim-open-toolkit/samples/nrc/questions.txt --out poc/results/unattended/<date>/new-run1.md --results poc/results/unattended/<date>/new-run1.json
```

`score_unattended.py` scores any number of result files against `results/expected_answers.json`
with one deterministic rule per question and prints the rule beside each verdict; `--markdown`
writes the table. The paper's Table 4 (version 2) is its output over the committed runs:

```bash
python poc/score_unattended.py poc/results/unattended/2026-10-04/*.json --markdown poc/results/unattended/2026-10-04/scores.md
```

See [../paper/paper-v2.md](../paper/paper-v2.md) for the version 2 write-up,
[../paper/06-proof-of-concept.md](../paper/06-proof-of-concept.md) for the version 1 write-up and
[../paper/poc-gap-report.md](../paper/poc-gap-report.md) for what did not work or was not done.
