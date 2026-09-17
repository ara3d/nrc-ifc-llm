# Storing, Displaying, and Querying Building Analytics on IFC Models with an LLM Agent Layer

_Christopher Diggins, Ara 3D / Studio 2.5, for the National Research Council of Canada. Draft of 2026-09-16._

## Abstract

Building performance analytics such as embodied carbon, operational carbon, and energy use
intensity are usually computed by tools that sit outside the building information model. The
results end up in spreadsheets and reports that cannot be joined back to the geometry, cannot be
validated against an information requirement, and cannot be asked about in plain language.

This paper examines three connected questions for openBIM workflows built on the Industry
Foundation Classes (IFC): where analytics should be stored so that they travel with the model,
how they should be displayed on the geometry, and how a large language model (LLM) can be placed in
front of an enriched model so that people can query it in natural language.

We compare twelve storage options available within the IFC 4.3 schema and recommend a
three-layer approach: scalar summary values in custom property sets at element, space, storey,
and building level; a reference from the IFC file to a richer external columnar dataset joined
on `GlobalId`; and a small metric dictionary that fixes names, units, and lifecycle stages so
that queries resolve reliably. We survey display techniques and open-source viewers, and
recommend colour mapping and aggregated views driven by the same tables the analytics are
stored in.

For the query layer we argue against giving an LLM the raw IFC file, and for a small typed,
read-only tool surface exposed over the Model Context Protocol (MCP). We describe an
implementation that converts IFC to the columnar BIM Open Schema, loads it into DuckDB, and
exposes 29 tools, and a dataflow graph in which the agent builds queries, colourings, and rule
checks with the same four editing operations a person uses.

The proof of concept was carried out on the buildingSMART Duplex Apartment model. A rule
checker driven by a machine-readable provision file evaluated four accessible-door-clearance
rules over 14 doors, produced 56 verdicts in all four categories with per-element evidence,
matched an independently derived ground truth exactly, produced byte-identical output across
repeated runs, and recorded a human override inside the IFC file in a form that can be removed
to restore the original byte for byte. A second case study, natural-language questions over the
same model enriched with carbon and energy analytics, is specified here and will be reported in
the next revision.

We close with the limitations of the work, the extensions the statement of work anticipates,
including knowledge graphs and world-model substrates, and a roadmap for an open-source
viewer in which selection, colouring, and property write-back are first-class agent operations.
