# 10. Conclusion

The question the engagement set was how building analytics computed outside IFC can be stored
with the model, shown on its geometry, and asked about in plain language. The answer this paper
gives has three parts that fit together.

**Store summaries in the file and the full data beside it.** Custom property sets carry the
scalar values that people look at, with units, stage, scenario, and run id in every set, at
element, space, storey, and building level. An `IfcDocumentReference` points to a long-format
Parquet table joined on `GlobalId` for everything else. A short metric dictionary ties the two
together. Writing is done as a byte-exact patch, so that an enriched file differs from the
original only in the entities that were added, and those can be removed to recover the original
exactly.

**Display from tables, not from the file.** A value table joined on `GlobalId` drives colour,
selection detail, and per-storey aggregates from one description. Unmatched elements are drawn
grey so that missing data is visible.

**Put the language model behind tools.** A small, typed, read-only tool surface over a columnar
copy of the model lets the model write queries that are correct, checkable, and cheap. Answers
carry their derivation. Compliance rules are queries with a verdict column, and absence of data
is a verdict, never a silent pass.

The executed case study showed the pipeline working end to end on a public model without the
language model in the loop: four rules from a machine-readable file, 56 verdicts in four
categories with evidence, an exact match to independently derived ground truth, hash-identical
output across runs, and a human override recorded in the IFC and removed again byte for byte.
The remaining case study, natural-language questions over the same model enriched with carbon
and energy values, is specified and will be reported in the next revision, together with the
viewer comparison.

What the client gains is not a viewer or a checker but a shape for the data: a row keyed by
`GlobalId` that can be a carbon value, a verdict, or an override, and that can be coloured,
summed, asked about, validated by an IDS, and written back. Everything in Sections 8 and 9,
from IDS alignment to knowledge graphs to a bidirectional viewer, builds on that shape rather
than replacing it.
