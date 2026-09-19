# 9 Limitations

The limitations are stated here in one place, so that the results of Section 8 are not read as more than they are.

## 9.1 Limitations of the proof of concept

**One public model.** Both case studies use the Duplex Apartment model, which is small, having two storeys and 14 doors, and whose authoring conventions, in particular Revit family names that encode dimensions, assisted the ground-truth step. NRC's own models will not necessarily encode dimensions in names, and the measured-against-declared rule DC-M1 is likely to require a geometric measurement in place of the name.

**One model, one run.** Case study A was answered twice, once by the author choosing tool calls by hand and once by a single unattended run of one language model, `gpt-5`, on 2026-09-18. Four of eight matched, and the three misses trace to the aggregate naming of Annex A rather than to the tool surface, as stated in Section 8.2. One run is not a measurement of reliability, and repeated runs, other models, and the renamed aggregate sets are required before an accuracy figure may be quoted.

**Synthetic analytics.** The carbon and energy values were generated from per-type base values with a hash jitter, and the operational columns originate in a dataset made for viewer testing. They have the correct shape, units, and join key, but they are not derived from an analysis tool. The provenance fields will carry real run identifiers only once NRC supplies a dataset.

**Storey resolution through relations was incomplete in the recorded session.** In the converted model, elements inside assemblies, such as stair flights, railings, and members, are reached through `MemberOf` rather than `ContainedIn`, and the Q2 query missed ten of them, which reversed a marginal comparison. The toolkit now exposes a `StoreyOfEntity` view that walks containment, aggregation, and membership, and which reaches all 103 Level 1 elements as shown in Figure 10, but the recorded session predates the view and is retained as recorded. Storey-level answers should still be taken from the written aggregates where these exist.

**Leaf width rather than clear width.** Rule DC-W1 tests `OverallWidth`, which is the door leaf. The clear width required by the code subtracts frame, stops, and hinge-side projection, and under a strict reading the six 864 mm doors could fail. DC-W2 is the honest placeholder, in that it demands an authored `ClearWidth` and returns inconclusive where this is absent.

**Placement-level geometry.** The zone rule DC-Z1 composes exact placement transforms but tests furnishing placement origins against an axis-aligned box rather than meshing every obstacle. The mesh path, through `ifc_volume` and `ifc_bounds`, exists in the toolkit but was not wired into the checker.

**Illustrative citations.** The rule file's references to NBC 2020 convey the shape of a real provision. They are not reproductions of code text and have not been reviewed by a code authority.

## 9.2 Limitations of the storage recommendation

**Custom property sets are a convention rather than a standard.** Layer 1 works because the names are agreed. Two organisations that both write `Pset_NRCEmbodiedCarbon` with different lifecycle stages will produce files that appear compatible and are not. The metric dictionary of Layer 3 and an IDS specification are the mitigations, and neither is yet implemented.

**Aggregates share the element property names.** As reported in Section 8.2, the storey and building sets carry the same property names as the element sets, so that a sum or ranking which does not exclude the container classes counts an aggregate as an element. The aggregate sets should be renamed, the generator and enrichment rerun, and the expected answers recomputed, before any accuracy figure is quoted.

**Typed values in write-back.** The dataflow node `sink.writePsets` wrote every value as `IFCTEXT` at the time the proof of concept was run, which is why the enrichment called the library directly. The node now takes an optional `valueType` column, accepting `Real`, `Integer`, `Boolean`, `Label`, `Identifier`, or `Text`, and the seeded graph `nrc-enrich-run` writes `psets_to_write.csv` with its types; the enrichment reported in Section 8.2 was not rerun through it.

**IFC units.** The recommendation places units in property names rather than relying on `IfcUnitAssignment`. This is robust but redundant, and a reviewer aligned with the IFC unit model may object.

**External references are able to break.** Layer 2 depends upon the referenced file being delivered with the IFC. The checksum in the reference detects substitution but not absence.

## 9.3 Limitations of the query layer

**No measured accuracy on the target task.** The figures reported in Section 7.4 were obtained on the toolkit's own test database and not on carbon and energy questions over an enriched IFC. They show that the approach works; they are not a measurement of this project's acceptance criterion.

**Ambiguity is not always surfaced.** On questions admitting no single correct reading, such as "the biggest rooms" where area is null for some rooms, the models tested chose an interpretation rather than asking. The host's post-evaluation check catches empty answers and not wrong interpretations.

**Windows only.** The IFC loader, and therefore the MCP server and the write-back path, target `net8.0-windows`. The engine and schema libraries are cross-platform, but the full proof of concept cannot yet be run on Linux or macOS.

**Local and single-user.** The host is a local process with no authentication, serving one request at a time. This is appropriate to a proof of concept and is not appropriate to a shared service.

## 9.4 Limitations of the display recommendation

The viewer comparison in Table 5 has one row obtained from the test kit, that of the toolkit's own viewer. For the other viewers the recommendation rests upon documented capabilities rather than upon the kit's results, and no screenshots have been captured. The toolkit row is further the only one whose colouring from an external table is a dataflow join rather than a script, which favours it on that column by construction.
