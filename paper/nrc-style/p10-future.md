# 10 Future directions

The statement of work [20] asks for complementary architectural patterns, including knowledge graphs and world-model substrates, as possible extensions beyond file-based IFC exchange. This section covers those patterns together with the nearer-term items that the proof of concept left open.

## 10.1 Near term: closing the gaps in this report

Five items are recommended in the near term:

1. The storey and building aggregate sets should be renamed as stated in Section 9.2, the values regenerated, the model re-enriched, and the unattended questions rerun, before any match count is quoted as a measure of accuracy;
2. The viewer test kit should be run through the shortlist of Table 5, beginning with Bonsai, and screenshots captured;
3. Both case studies should be repeated on an NRC model with a real analytics dataset, once one is supplied;
4. Value types should be passed through `sink.writePsets`, so that numeric analytics written from the dataflow graph are `IFCREAL` rather than text;
5. The existing volume and bounds tools should be wired into the zone rule, so that obstacles are tested by geometry rather than by placement origin.

## 10.2 IDS as the rule format

The door demonstration uses a purpose-built JSON rule schema, because it required requirement kinds, namely zone clash and measured against declared, which IDS 1.0 [2] does not express. The property-threshold rules DC-W1 and DC-W2 are, however, exactly what IDS was designed for, comprising an applicability, `IFCDOOR`, and a requirement, a property with a minimum value. Two steps follow.

Layer 1 of the storage recommendation should be expressed as an IDS specification, requiring that every element of the covered classes carry the NRC property sets with values of the correct type, and delivered models should be validated against it with an existing IDS checker before any analytics query is run. Further, the property-threshold rule kind should be mapped to IDS, so that a rule file is able to carry IDS requirements alongside the geometric kinds which IDS cannot express, and so that the checker's verdicts and an IDS validator's report agree on the same door.

## 10.3 Knowledge graphs and linked building data

The columnar tables described in this report are a graph flattened into edge lists, comprising entities and a relations table with a closed vocabulary. Converting them to RDF using BOT [4] and the IFC-LBD mappings is mechanical, and the analytics rows of Layer 2 become triples with the metric dictionary of Layer 3 as their predicate vocabulary.

What this gains is joins outside the building: to product EPD databases, to a climate zone, to an organisation's asset register, and to the regulation text itself. What it costs is tooling. SPARQL endpoints and reasoners are less familiar to the client's users than DuckDB and Parquet, and a language model writes SQL more reliably than SPARQL at present. It is therefore recommended that the columnar form be retained as the working representation and that an RDF export be published from it, rather than that RDF be made the store.

## 10.4 World-model substrates

The term "world model" carries two nearly opposite meanings for two audiences. To machine-learning researchers it denotes a learned, predictive, probabilistic model of an environment. To BIM practitioners it denotes an authored, explicit, complete database of the built asset which transcends any one authoring tool. The toolkit's design note on terminology [34] maps the collision.

The work reported here lies on the second side, being a declarative substrate in which every value has a provenance and every verdict has evidence, and that is the appropriate foundation for the first. A learned model which predicts embodied carbon from partial geometry, or which proposes a retrofit, requires a ground truth against which to be trained and checked, and the tables, run records, and byte-exact diffs described here are what such a ground truth looks like. The extension the client should watch for is therefore not the replacement of the IFC by a neural model, but the training and auditing of predictors against the enriched, versioned models that this pipeline produces.

## 10.5 Federated and versioned model collections

Every IFC MCP server surveyed [24], including the one described here, operates upon one loaded file. A portfolio, or one building across design stages, requires element sets that persist across sessions, queries that span several models, a notion of epoch so that "carbon before and after the change" is a single question, and stable identifiers that survive the passage from Revit to IFC to BOS to a lakehouse. The dataflow store and the run records are a beginning on the query-history side. The identifier problem is the harder one and remains unsolved in the industry.

## 10.6 Design records under version control

A longer-horizon vision, sketched in the repository [28], treats a project as a repository, with checkpoints, design options as branches, proposed changes as reviewable requests, automated validation as a pipeline, and decisions as first-class records linked to the evidence that supported them. The enriched IFC files, rule files, verdict tables, and run records described in this report are the artefacts that such a system would version, and the byte-exact write-back path is what renders an IFC diff readable enough to review.
