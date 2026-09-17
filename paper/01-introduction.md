# 1. Introduction

## 1.1 The problem

The National Research Council of Canada (NRC) produces analytics on building models: operational
carbon, embodied carbon, energy use, and related performance indicators. These are computed by
simulation and life-cycle assessment tools whose inputs may be derived from an IFC model but whose
outputs are not written back to it. The numbers live in the tools' own databases, in CSV exports,
and in PDF reports.

Three things become hard once the results have left the model:

1. **Showing them.** A designer cannot open the model and see which walls carry the most embodied
   carbon, because the model does not know.
2. **Reusing them.** A downstream tool, or a later project phase, cannot find the results without
   the original tool and its project file. There is no standard place to look.
3. **Asking about them.** Questions such as "what is the total operational carbon on Level 2" or
   "which doors fail the clearance rule" require someone who knows both the analysis tool and the
   model.

The IFC schema has mechanisms that could hold these results. The Information Delivery
Specification (IDS) can state which results a delivered model must carry. Large language models
can turn a question into a query. None of these pieces is new, but there is no settled practice
for putting them together, and the obvious approach, handing the LLM the IFC file, does not
work at the scale of real models.

## 1.2 Questions this paper answers

The statement of work sets three objectives and a publication. The paper is organised around
them.

- **Storage.** Which IFC mechanisms should carry analytics, at component, zone, storey, and
  building level, so that the data is portable, reusable, and queryable? (Section 3)
- **Display.** How should analytics be shown on IFC geometry, and which freely available viewers
  and libraries support it? (Section 4)
- **Query.** How should an LLM-based layer be built so that it answers natural-language questions
  about an enriched model correctly, and so that its answers can be checked? (Section 5)
- **Evidence.** What does a working proof of concept look like, and what did it find? (Section 6)

## 1.3 Contributions

1. A comparison of twelve storage options within IFC 4.3, ranked on portability, queryability,
   interoperability, and scalability, with a three-layer recommendation and concrete property-set
   definitions (Section 3, Appendix A).
2. An argument, supported by an implementation, that the LLM should sit behind a small typed
   read-only tool surface over a columnar copy of the model rather than reading the IFC file, and
   a description of that surface (Section 5, Appendix C).
3. A byte-exact write-back path for property sets, so that analytics, verdicts, and human
   overrides can be added to a client's IFC file without altering any byte the writer did not
   intend to change (Sections 3.5 and 6.3).
4. An executed, reproducible demonstration on a public model: a machine-readable provision file,
   a checker, four verdict categories, independently derived ground truth, hash-verified
   determinism, and a reversible override recorded in the IFC (Section 6).
5. A roadmap for an open bidirectional viewer in which selection, colouring, viewpoints, and
   write-back are operations an agent can call (Section 9).

## 1.4 Scope and exclusions

The proof of concept is a minimal one. It is not a production viewer, not a certified compliance
checker, and not a replacement for the client's analysis tools. Geometry authoring is out of
scope. The models used are public samples; NRC's own models and analytics datasets, once
supplied, will be used to repeat the runs reported in Section 6.

## 1.5 How to read this paper

Sections 3 and 4 are the options analysis (deliverable D1) and can be read on their own.
Sections 5 and 6 describe the proof of concept (deliverable D2). Sections 7 to 9 look forward.
Readers who want only the recommendations should read Sections 3.6, 4.4, and 5.6.
