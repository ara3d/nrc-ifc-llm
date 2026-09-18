# 7. Limitations

The limitations are stated here in one place so that the results in Section 6 are not read as
more than they are.

## 7.1 Of the proof of concept

**One public model.** Both case studies use the Duplex Apartment. It is small (two storeys,
14 doors) and its authoring conventions (Revit family names that encode dimensions) helped the
ground-truth step. NRC's own models will not necessarily encode dimensions in names, and the
measured-versus-declared rule (DC-M1) will need a geometric measurement in its place.

**Case study A was run by the author acting as the agent.** The questions were answered by
choosing MCP tool calls by hand and recording them, not by an autonomous agent loop in a chat
client. This shows that the tool surface can answer the questions; it does not measure how
often an unattended language model would choose the right calls.

**Synthetic analytics.** The carbon and energy values were generated from per-type base values
with a hash jitter, and the operational columns come from a dataset made for viewer testing.
They have the right shape, units, and join key but are not from an analysis tool. Provenance
fields will carry real run identifiers only once NRC supplies a dataset.

**Storey resolution through relations is incomplete.** In the converted model, elements inside
assemblies (stair flights, railings, members) are reached by `PartOf`, not `ContainedIn`, and
the Q2 query missed ten of them, which flipped a marginal comparison. Storey-level answers
should come from the written aggregates, or the query layer needs a storey-of-element view
that walks both relations.

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

**Typed values in write-back.** The dataflow node `sink.writePsets` currently writes every value
as `IFCTEXT`. The library beneath it supports `IFCREAL`, `IFCINTEGER`, `IFCBOOLEAN`, `IFCLABEL`,
and `IFCIDENTIFIER`, and the door demonstration uses them, but the node has not been updated
to pass the type through. Numeric analytics written through the node would read back as text.

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

The viewer comparison in Section 4.3 has not been run. The recommendation rests on documented
capabilities of each viewer, not on the test kit's results, and no screenshots have been
captured.
