# 7. Limitations

The limitations are stated here in one place so that the results in Section 6 are not read as
more than they are.

## 7.1 Of the proof of concept

**One public model.** Both case studies use the Duplex Apartment. It is small (two storeys,
14 doors) and its authoring conventions (Revit family names that encode dimensions) helped the
ground-truth step. NRC's own models will not necessarily encode dimensions in names, and the
measured-versus-declared rule (DC-M1) will need a geometric measurement in its place.

**One model, one run.** Case study A was answered twice: by the author choosing tool calls
by hand, and by one unattended run of one language model (`gpt-5`) on 2026-09-18. Four of eight
matched, and the three misses trace to the aggregate naming in Appendix A rather than to the
tool surface (Section 6.2). One run is not a measurement of reliability; repeated runs, other
models, and the renamed aggregate sets are needed before an accuracy figure can be quoted.

**Synthetic analytics.** The carbon and energy values were generated from per-type base values
with a hash jitter, and the operational columns come from a dataset made for viewer testing.
They have the right shape, units, and join key but are not from an analysis tool. Provenance
fields will carry real run identifiers only once NRC supplies a dataset.

**Storey resolution through relations was incomplete in the recorded session.** In the
converted model, elements inside assemblies (stair flights, railings, members) are reached by
`MemberOf`, not `ContainedIn`, and the Q2 query missed ten of them, which flipped a marginal
comparison. The toolkit now exposes a `StoreyOfEntity` view that walks containment,
aggregation, and membership (Figure 10 reaches all 103 Level 1 elements), but the recorded
session predates it and is kept as recorded. Storey-level answers should still come from the
written aggregates where they exist.

**Leaf width, not clear width.** Rule DC-W1 tests `OverallWidth`, which is the door leaf. The
code's clear width subtracts frame, stops, and hinge-side projection; under a strict reading
the six 864 mm doors could fail. DC-W2 is the honest placeholder: it demands an authored
`ClearWidth` and returns inconclusive when absent.

**Placement-level geometry.** The zone rule DC-Z1 composes exact placement transforms but tests
furnishing placement origins against an axis-aligned box rather than meshing every obstacle. The
mesh path (`ifc_volume`, `ifc_bounds`) exists in the toolkit but was not wired into the checker.

**Illustrative citations.** The rule file's NBC references convey the shape of a real provision.
They are not reproductions of code text and have not been reviewed by a code authority.

## 7.2 Of the storage recommendation

**Custom property sets are a convention, not a standard.** Layer 1 works because the names are
agreed. Two organisations that both write `Pset_NRCEmbodiedCarbon` with different lifecycle
stages will produce files that look compatible and are not. The metric dictionary (Layer 3)
and an IDS specification are the mitigations, and neither is implemented yet.

**Typed values in write-back.** The dataflow node `sink.writePsets` wrote every value as
`IFCTEXT` when the proof of concept ran, which is why the enrichment used the library directly.
The node now takes an optional `valueType` column (`Real`, `Integer`, `Boolean`, `Label`,
`Identifier`, `Text`) and the seeded graph `nrc-enrich-run` writes `psets_to_write.csv` with
its types; the enrichment reported in Section 6.2 was not rerun through it.

**IFC units.** The recommendation puts units in property names rather than relying on
`IfcUnitAssignment`. This is robust but redundant, and a reviewer aligned with the IFC unit
model may object.

**External references can break.** Layer 2 depends on the referenced file being delivered with
the IFC. The checksum in the reference detects substitution but not absence.

## 7.3 Of the query layer

**No measured accuracy on the target task.** The accuracy figures in Section 5.4 are from the
toolkit's own test database, not from carbon and energy questions over an enriched IFC. They
show that the approach works; they are not a measurement of this project's acceptance
criterion.

**Ambiguity is not always surfaced.** On questions with no single right reading ("the biggest
rooms" when area is null for some), the models tested chose an interpretation rather than
asking. The host's post-evaluation check catches empty answers, not wrong interpretations.

**Windows only.** The IFC loader, and therefore the MCP server and the write-back path, target
`net8.0-windows`. The engine and schema libraries are cross-platform, but the full proof of
concept cannot yet run on Linux or macOS.

**Local, single user.** The host is a local process with no authentication and one request at
a time. This is appropriate for a proof of concept and not for a shared service.

## 7.4 Of the display recommendation

The viewer comparison in Section 4.3 has one row from the test kit, the toolkit's own viewer.
For the other viewers the recommendation rests on documented capabilities, not on the kit's
results, and no screenshots have been captured. The toolkit row is also the only one whose
"colour from an external table" is a data-flow join rather than a script, which favours it on
that column by construction.
