# Technical Paper: Storing, Displaying, and Querying Building Analytics on IFC Models

_Deliverable D3 of the Studio 2.5 / NRC engagement. Initial draft, 2026-09-16._

This folder holds the paper as one Markdown file per section so that sections can be
drafted, reviewed, and revised independently. Read the sections in the order below.
`figures/` holds screenshots and diagrams referenced from the text.

## Sections

| # | File | Status |
|---|---|---|
| 0 | [Abstract](00-abstract.md) | Draft |
| 1 | [Introduction](01-introduction.md) | Draft |
| 2 | [Background](02-background.md) | Draft |
| 3 | [Storage options and recommendation](03-storage-options.md) | Draft, derived from the options brief |
| 4 | [Display options and recommendation](04-display-options.md) | Draft, needs viewer matrix and screenshots |
| 5 | [The LLM and agent layer](05-llm-agent-layer.md) | Draft |
| 6 | [Proof of concept and results](06-proof-of-concept.md) | Both case studies executed; A with synthetic data |
| 7 | [Limitations](07-limitations.md) | Draft |
| 8 | [Future directions](08-future-directions.md) | Draft |
| 9 | [Roadmap for an open bidirectional viewer](09-viewer-roadmap.md) | Draft |
| 10 | [Conclusion](10-conclusion.md) | Draft |
| A | [Appendix A: property-set definitions](appendix-a-property-sets.md) | Draft |
| B | [Appendix B: rule file schema](appendix-b-rule-schema.md) | Draft |
| C | [Appendix C: MCP tool surface](appendix-c-tool-surface.md) | Draft |
| R | [References](references.md) | Draft |
| G | [Proof-of-concept gap report](poc-gap-report.md) | What the executed run did not cover |

## Status of the evidence

Everything in section 6 marked **executed** is backed by tests and commits pinned in
[bos-validation-evidence.md](../bos-validation-evidence.md) and
[door-clearance-demo.md](../door-clearance-demo.md). Case study A was executed on 2026-09-17 with synthetic data; its scripts and transcript are in
[poc/](../poc/README.md) and its open items are in the [gap report](poc-gap-report.md).

## Building a single document

Concatenate the files in table order to produce one Markdown file for conversion to PDF or
Word:

```bash
cat 00-abstract.md 01-introduction.md 02-background.md 03-storage-options.md 04-display-options.md 05-llm-agent-layer.md 06-proof-of-concept.md 07-limitations.md 08-future-directions.md 09-viewer-roadmap.md 10-conclusion.md appendix-a-property-sets.md appendix-b-rule-schema.md appendix-c-tool-surface.md poc-gap-report.md references.md > paper.md
```

## Source material

The paper draws on the repository documents listed in the top-level
[README](../README.md) and on code in the
[bim-open-toolkit](https://github.com/ara3d/bim-open-toolkit) repository. Code examples are
quoted from that repository and are current as of its commit `71790a7`.
