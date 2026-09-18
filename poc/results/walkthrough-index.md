# NRC walkthrough output

Generated 2026-09-18T21:58:55.613Z by scripts/nrc-walkthrough.mjs at toolkit commit 13463b2 in 41 s.
Duplex first (public IFC, synthetic analytics), then Snowdon (private BOS and DuckDB export). See docs/nrc-walkthrough.md for the narrative.

## Snowdon: 3D recipes

The private Snowdon Towers BOS through samples/snowdon-analyses/snowdon-toolkit.json (4 captures in snowdon/).

- [snowdon-1-categories.png](snowdon/snowdon-1-categories.png): Snowdon Towers coloured by category through view3d.categoryStyle. (456,598 instances · orbit / pan / zoom)
- [snowdon-2-cutaway.png](snowdon/snowdon-2-cutaway.png): A horizontal section (view3d.section) through the same model. (456,598 instances · orbit / pan / zoom)
- [snowdon-3-exploded.png](snowdon/snowdon-3-exploded.png): Categories fanned apart (view3d.explode). (456,598 instances · orbit / pan / zoom)
- [snowdon-4-plan.png](snowdon/snowdon-4-plan.png): Plan projection (view3d.projection) of the sectioned model. (456,598 instances · orbit / pan / zoom)

## Snowdon: DuckDB workflows

The tables host over the Snowdon typed export (2 captures in snowdon/).

- [snowdon-5-door-schedule.png](snowdon/snowdon-5-door-schedule.png): The Snowdon door schedule: two duck.query nodes, a join, and a sort over the typed DuckDB export.
- [snowdon-6-room-distribution.png](snowdon/snowdon-6-room-distribution.png): Rooms per storey from the same export.

## Snowdon: MCP connectivity

The dataflow MCP server over stdio builds and evaluates a door-schedule graph from tool calls alone: FAIL.
