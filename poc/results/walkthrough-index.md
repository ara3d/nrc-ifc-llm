# NRC walkthrough output

Generated 2026-09-18T22:45:53.051Z by scripts/nrc-walkthrough.mjs at toolkit commit 7e3192e in 213 s.
Duplex first (public IFC, synthetic analytics), then Snowdon (private BOS and DuckDB export). See docs/nrc-walkthrough.md for the narrative.

## Duplex: figures

Host: bim profile over samples/nrc (10 captures in duplex/, index in duplex/index.md).

- [figure-2-storey-carbon-chart.png](duplex/figure-2-storey-carbon-chart.png): Figure 2. Embodied and operational carbon per storey (synthetic values) as a bar chart from a chart.bar node over the storey CSV.
- [figure-3-storey-carbon-table.png](duplex/figure-3-storey-carbon-table.png): Figure 3. The same aggregates in the Table tab.
- [figure-4-property-values-table.png](duplex/figure-4-property-values-table.png): Figure 4. The 2,438 rows the byte-exact writer turned into IFCPROPERTYSINGLEVALUE entities.
- [figure-5-3d-operational-carbon.png](duplex/figure-5-3d-operational-carbon.png): Figure 5. duplex-enriched.ifc coloured by operational carbon (viridis, normalised over the column); instances without a value are grey. (660 instances · orbit / pan / zoom)
- [figure-6-3d-embodied-carbon.png](duplex/figure-6-3d-embodied-carbon.png): Figure 6. The same model coloured by embodied carbon A1-A3; the roof has no value and stays grey. (660 instances · orbit / pan / zoom)
- [figure-7-3d-category.png](duplex/figure-7-3d-category.png): Figure 7. One colour per analysis category (category10 palette, nine categories). (660 instances · orbit / pan / zoom)
- [figure-8-3d-dc-w1-verdicts.png](duplex/figure-8-3d-dc-w1-verdicts.png): Figure 8. Rule DC-W1 (door leaf width at least 850 mm) evaluated by check.rule over the model's own OverallWidth, 8 pass and 6 fail, coloured on the doors. (660 instances · orbit / pan / zoom)
- [figure-9-dc-w1-verdict-table.png](duplex/figure-9-dc-w1-verdict-table.png): Figure 9. The verdict table behind Figure 8: one row per door with the width read and the citation.
- [figure-10-storey-of-element.png](duplex/figure-10-storey-of-element.png): Figure 10. Elements per storey from the StoreyOfEntity view, which walks ContainedIn, PartOf, and MemberOf: Level 1 has 103, the count the hand-driven session missed.
- [figure-13-picked-element-properties.png](duplex/figure-13-picked-element-properties.png): Figure 13. A picked wall: the 3D pane lists its property sets, including the Pset_NRC sets the enrichment wrote. (Selected entity 5498)
