# 8. Future directions

The statement of work asks for complementary architectural patterns, including knowledge graphs
and world-model substrates, as possible extensions beyond file-based IFC exchange. This section
covers those and the nearer-term items that the proof of concept left open.

## 8.1 Near term: closing the gaps in this paper

1. **Run case study A** with the question list in Section 6.2 and record expected versus
   observed per question.
2. **Run the viewer test kit** through the shortlist in Section 4.3 and capture screenshots.
3. **Repeat both case studies on an NRC model** with a real analytics dataset once supplied.
4. **Pass value types through `sink.writePsets`** so that numeric analytics written from the
   dataflow graph are `IFCREAL`, not text.
5. **Mesh-accurate clearance.** Wire the existing volume and bounds tools into the zone rule so
   that obstacles are tested by geometry, not by placement origin.

## 8.2 IDS as the rule format

The door demonstration uses a purpose-built JSON rule schema because it needed requirement kinds
(zone clash, measured versus declared) that IDS 1.0 does not express. But the property-threshold
rules DC-W1 and DC-W2 are exactly what IDS was designed for: an applicability (`IFCDOOR`) and a
requirement (a property with a minimum value). Two steps follow.

- Express Layer 1 of the storage recommendation as an IDS specification: every element of the
  covered classes must carry the NRC property sets with values of the right type. Validate
  delivered models against it with an existing IDS checker before any analytics query is run.
- Map the property-threshold rule kind to IDS, so that a rule file can carry IDS requirements
  alongside the geometric kinds IDS cannot express, and so that the checker's verdicts and an
  IDS validator's report agree on the same door.

## 8.3 Knowledge graphs and linked building data

The columnar tables in this paper are a graph flattened into edge lists: entities, and a
relations table with a closed vocabulary. Converting them to RDF using BOT and the IFC-LBD
mappings is mechanical, and the analytics rows in Layer 2 become triples with the metric
dictionary (Layer 3) as their predicate vocabulary.

What this buys is joins outside the building: to product EPD databases, to a climate zone, to
an organisation's asset register, to the regulation text itself. What it costs is tooling. SPARQL
endpoints and reasoners are less familiar to the client's users than DuckDB and Parquet, and an
LLM writes SQL more reliably than SPARQL today. The recommendation is to keep the columnar form
as the working representation and to publish an RDF export from it, rather than to make RDF the
store.

## 8.4 World-model substrates

"World model" means two nearly opposite things to two audiences. To machine-learning
researchers it is a learned, predictive, probabilistic model of an environment. To BIM
practitioners it is an authored, explicit, complete database of the built asset that transcends
any one authoring tool. The toolkit's design note on
[AEC world-model terminology](https://github.com/ara3d/bim-open-toolkit/blob/71790a7/docs/aec-world-model-terminology.md)
maps the collision.

The work in this paper is on the second side: a declarative substrate where every value has a
provenance and every verdict has evidence. That is the right foundation for the first side. A
learned model that predicts embodied carbon from partial geometry, or proposes a retrofit, needs
a ground truth to be trained and checked against, and the tables, run records, and byte-exact
diffs described here are what such a ground truth looks like. The extension the client should
watch for is therefore not "replace the IFC with a neural model" but "train and audit
predictors against the enriched, versioned models this pipeline produces".

## 8.5 Federated and versioned model collections

Every IFC MCP server surveyed, including the one described here, works on one loaded file. A
portfolio, or one building across design stages, needs: element sets that persist across
sessions; queries that span several models; a notion of epoch so that "carbon before and after
the change" is one question; and stable identifiers that survive the trip from Revit to IFC to
BOS to a lakehouse. The dataflow store and run records are a start on the query-history side.
The identifier problem is the hard one and is unsolved in the industry.

## 8.6 Design records under version control

A longer-horizon vision, sketched in
[ai_assisted_architecture_design_system.md](../ai_assisted_architecture_design_system.md), treats
a project as a repository: checkpoints, design options as branches, proposed changes as
reviewable requests, automated validation as a pipeline, and decisions as first-class records
linked to the evidence that supported them. The enriched IFC files, rule files, verdict tables,
and run records of this paper are the artefacts such a system would version. The byte-exact
write-back path is what makes an IFC diff readable enough to review.
