# 8 Proof of concept and results

The proof of concept comprises two case studies on the same public model. Case study A is the acceptance criterion of the statement of work [20], namely natural-language questions answered against an IFC model enriched with analytics. Case study B applies the same storage and query machinery to code compliance. Both were carried out on the buildingSMART Duplex Apartment model [18], `duplex.ifc`, of 38,898 STEP entities.

It should be noted that case study B, reported in Section 8.3, was executed on 2026-08-04 and independently re-run on 2026-08-05, and that every claim within it is supported by a test or a commit pinned in the demonstration record [26]. Case study A, reported in Section 8.2, was executed on 2026-09-17 with synthetic analytics; its scripts, data, and transcript are held in the repository, and what it did not cover is listed in Annex D.

## 8.1 Model, data, and toolchain

The model, data, and toolchain are given in Table 6.

**Table 6** Model, data, and toolchain of the proof of concept.

| Item | Detail |
|---|---|
| Model | `duplex.ifc`, buildingSMART Duplex Apartment, IFC2X3, 38,898 entities, 2 storeys |
| Elements with analytics | 268, keyed by `GlobalId`, in `analytics_dataset_with_levels.csv` |
| Analytics columns | `operational_carbon`, `energy_intensity`, `category`, `Level` |
| Doors | 14, of which 6 on Level 1 and 8 on Level 2 |
| Furnishing elements | 61, treated as potential obstacles |
| Toolchain | BIM Open Toolkit at commit `71790a7`; .NET 8; DuckDB |

The toolchain itself is exercised end to end by automated tests before either case study is run. The IFC-to-BOS conversion, the table listing, the paged SQL, the read-only enforcement, the text views, the export, and a cross-check that the storey count obtained from SQL equals the storey count obtained from the entity tools are all asserted against the FZK-Haus model [19], and the server is run as a live subprocess over stdio. The validation evidence inventory [25] lists the tests and commits.

## 8.2 Case study A: natural-language questions over an enriched model

This study was executed on 2026-09-17. The analytics are synthetic, as stated in Section 9.1: each physical element received a type-based embodied carbon value with a deterministic jitter, and the test kit's operational carbon and energy intensity columns were reused. The roof deliberately received no embodied-carbon set.

**Procedure.** The procedure comprised four steps. First, a generator script produced Layer 1 values for the 218 physical elements, openings excluded, together with storey and building aggregates, a Layer 2 long-format table, and a provenance set for the project, following Annex A. Second, a small .NET program wrote the values into a copy of the model with the byte-exact writer described in Section 5.5; the entity diff listed exactly the added entities, removing them restored the source byte for byte, and a second run produced identical bytes. Third, the expected answer to each question was computed from the CSV alone, without the IFC file and without the server. Fourth, the enriched model was opened through the IFC MCP server over HTTP, and the author, acting as the agent, asked each question by choosing tool calls, while a helper script recorded every call, its arguments, and its result verbatim before the answer was written.

The counts obtained from the enrichment are given in Table 7.

**Table 7** Enrichment counts for case study A.

| Item | Value |
|---|---|
| Source entities | 38,898 |
| Enriched entities | 42,664 |
| Property sets written | 664 |
| Property values written | 2,438 |
| Entities added | 3,766 |
| Diff exact, reversible, deterministic | Yes, yes, yes |

The property values were written as `IFCREAL`, `IFCLABEL`, `IFCIDENTIFIER`, and `IFCTEXT`, on 218 elements, 4 storeys, the building, and the project.

**Results of the hand-driven session.** All eight questions were answered from the file through the read-only SQL tool over the BOS text views. Seven of the returned values matched the expectation exactly, and Q2 did not, for a reason that the transcript makes visible. The comparison is given in Table 8.

**Table 8** Case study A, hand-driven session of 2026-09-17: expected against returned.

| # | Level | Question | Expected | Returned | Calls |
|---|---|---|---|---|---|
| Q1 | Building | Total operational carbon | 37,196.2 kgCO2e/yr | 37,196.2, from both the building aggregate and the sum of 218 elements | 2 |
| Q2 | Storey | Higher mean energy intensity, Level 1 or Level 2 | Level 2, marginally: L1 40.50, L2 40.56, over 103 and 93 elements | Level 1: 41.72 against 40.56, over 93 elements each; disagrees | 2 |
| Q3 | Component | Five highest operational carbon | Walls 412.0 and 410.8; cabinet 402.0; walls 399.7 and 398.6 | Same five, same order | 1 |
| Q4 | Component | Operational carbon of door `M_Single-Flush:0762 x 2032mm` | 54.0, the first of four | All four doors listed, 54.0 for the first, ambiguity stated | 1 |
| Q5 | Category | Operational carbon per class | Walls 17,547.4; slabs 5,816.9; furnishing 5,766.3 | Same, over all 14 classes | 1 |
| Q6 | Provenance | Which run, and when | run-2026-09-17-01, 2026-09-17 | Same, with tool, method, and dataset URI; 664 sets carry the run identifier | 2 |
| Q7 | Absence | Embodied carbon of the roof | Not available | Not available, with the two sets the roof does carry | 1 |
| Q8 | Storey | Embodied carbon per storey | L1 49,451.2; L2 48,696.8; T/FDN 11,761.3; Roof 5,821.0 | Same | 1 |

Two observations from the transcript matter more than the matches themselves.

The first concerns Q2, which required a second query and was nonetheless returned incorrectly. In the converted model, the `ContainedIn` relation points at the room, such as Kitchen or Bedroom 1, for elements inside a room, and at the storey for the remainder. The first query grouped by the direct container and produced a list of rooms. The agent stated this in the transcript and wrote a second query walking from room to storey, which reaches 93 of the 103 Level 1 elements, because ten stair, railing, and member parts are aggregated into assemblies rather than contained. The answer stated the caveat, but the conclusion drawn, that Level 1 is higher, is the opposite of the expectation over all elements, which is that Level 2 is higher by 0.06. The margin is small and the synthetic data makes the question artificial, but the lesson is likely to hold generally: a per-storey mean derived by the agent from relations is only as complete as the relation walk, and the storey aggregates written in Layer 1, which Q8 uses, exist precisely so that the answer need not depend upon it.

The second concerns Q4, which is ambiguous by name, four doors sharing the family name. The agent returned all four with their STEP identifiers and `GlobalId`s rather than choosing one silently.

**Mechanical replay.** The toolkit's `scripts/demo-ifc-mcp.mjs` replays the session's SQL for Q1, Q5, Q7, and Q8 over the IFC MCP server's stdio transport, which is the transport an MCP client uses, and checks each result against `expected_answers.json`. On 2026-09-18 all four matched. This establishes the connection and the tool surface end to end without a language model.

**Unattended run.** On 2026-09-18 the same eight questions were put verbatim to `gpt-5` through the toolkit's `bimopenmcp-ifc-ask` runner, with one fresh conversation per question, the IFC MCP server in process, and no human in the loop. The system prompt names the file, the views and their columns, and the rules, namely that every number is to come from a tool result and that "not available" is a valid answer. The run totalled 35 tool calls, 221,968 input tokens, and 30,144 output tokens, at toolkit commit `66df499`. The comparison is given in Table 9.

**Table 9** Case study A, unattended `gpt-5` run of 2026-09-18: expected against returned.

| # | Expected | Returned by `gpt-5` | Calls | Match |
|---|---|---|---|---|
| Q1 | 37,196.2 | 37,196.2, from the building's own aggregate | 3 | Yes |
| Q2 | Level 2, marginally: 40.50 against 40.56 | Level 2, 40.499 against 40.557, grouped through `StoreyOfEntity` | 4 | Yes, where the hand-driven session did not |
| Q3 | Walls 412.0 and 410.8; cabinet 402.0; walls 399.7 and 398.6 | The building, 37,196.2, and the four storeys: the query ranked every entity carrying the property, containers included | 3 | No |
| Q4 | 54.0, the first of four | All four doors with STEP identifiers, 54.0 for #8066, and a question returned as to which was intended | 4 | Yes |
| Q5 | Per analytics category: Wall 22,854.1, Floor 5,593.5, and so on | Per IFC class: IFCWALLSTANDARDCASE 17,547.4, IFCSLAB 5,816.9, and so on, over 16 rows that include the building and storey aggregates | 3 | Partly: the recorded session's grouping, with container rows not excluded |
| Q6 | run-2026-09-17-01, 2026-09-17 | Same, from `Pset_NRCAnalyticsProvenance` | 4 | Yes |
| Q7 | Not available | 1,838.5 kgCO2e A1 to A3, from the roof's `IFCSLAB` member, stating that the `IFCROOF` itself carries none | 11 | No, and informative |
| Q8 | L1 49,451.2; L2 48,696.8; T/FDN 11,761.3; Roof 5,821.0 | Exactly double each: 98,902.4; 97,393.6; 23,522.6; 11,642.0 | 3 | No |

Four questions matched, one matched partly, and three did not, and the three misses share one cause which matters more for the storage recommendation than for the agent. The Layer 1 aggregates written on the storey and building entities carry the same property set and property name as the element values. An agent that sums or ranks everything carrying `OperationalCarbon_kgCO2e_per_year` therefore counts the building and the storeys as elements, as in Q3 and Q5, and, when it groups elements by storey through `StoreyOfEntity`, adds the storey's own aggregate to its elements' sum and doubles every total, as in Q8. The hand-driven session avoided this by excluding the container classes in each query, which is the kind of knowledge a prompt is able to carry but a file should not require. Annex A should accordingly give the aggregate sets their own names, for example `Pset_NRCStoreySummary`, or their own property names, so that a sum over the element property cannot include an aggregate of itself.

Q7 is a different lesson. The generator wrote no set on the `IFCROOF`, but the roof is an assembly whose `IFCSLAB` member received values, and the agent found them, reported them, and stated which entity carries them. The expected answer of "not available" was the author's, and the agent's answer is the better one; the question should be read as concerning the roof assembly, and the absence test in the question list should use an element with no analysed descendants.

Q2 is the mirror image of the recorded session, in that the unattended agent used the storey view which the toolkit gained after that session, and obtained the expected ordering over all elements.

## 8.3 Case study B: door clearance, from code text to verdicts

This study was executed on 2026-08-04. It shows a building-code provision expressed as a machine-readable rule, executed by a checker against the model, with verdicts stored per element and a human override written back into the IFC. Figure 13 shows the three stages and the plan-view geometry of the zone rule.

![Figure 13](../figures/figure-1-door-clearance-pipeline.svg)

_Figure 13 The three stages of case study B: a code provision, its JSON rule, and the checker's verdict records, with the plan-view zone test of rule DC-Z1 and the verdict totals._

**Rules.** Four provisions modelled on the accessible-door requirements of NBC 2020 [6] were used, and are given in Table 10. The citations are labelled illustrative in the rule file and are not legal text.

**Table 10** The four door-clearance provisions modelled in case study B.

| Rule | Kind | Requirement |
|---|---|---|
| DC-W1 | Property threshold | `OverallWidth` of at least 850 mm |
| DC-W2 | Property threshold | `Pset_DoorCommon.ClearWidth` of at least 850 mm |
| DC-M1 | Measured against declared | Width encoded in the type name agrees with `OverallWidth` to within 25 mm |
| DC-Z1 | Zone unobstructed | Manoeuvring zone in front of the door, of depth equal to the door width, free of furnishing elements; applies to storey "Level 1" only |

Each rule in the JSON file carries an identifier, a citation, an applicability filter comprising entity type and optional storey, requirement parameters, and a sentence of verdict semantics. Annex B gives the schema and one full rule.

**Checker.** A small engine loads the rule file, evaluates every rule against every door, and emits one record per combination of door and rule, carrying the verdict and the evidence that produced it. Output is sorted by `GlobalId` and then by rule identifier, so that it does not depend on file order.

```csharp
public static IReadOnlyList<VerdictRecord> Evaluate(ModelFacts facts, RuleSet rules)
    => facts.Doors
        .SelectMany(door => rules.Rules.Select(rule => Evaluate(door, rule, facts)))
        .OrderBy(v => v.GlobalId, StringComparer.Ordinal)
        .ThenBy(v => v.RuleId, StringComparer.Ordinal)
        .ToList();
```

A property-threshold rule returns `Inconclusive` where the property is absent, and does not guess. The zone rule composes the door's full placement chain, rotation included, to build an axis-aligned zone box, and tests each furnishing element's placement origin against it.

**Ground truth.** Before the checker was written, a separate agent, in a separate commit, extracted every door's STEP identifier, `GlobalId`, name-encoded width and height from Revit family names such as `M_Single-Flush:0762 x 2032mm`, declared `OverallWidth` and `OverallHeight`, and containing storey [27]. All 14 doors carry both attributes; name-encoded and declared dimensions agree to the millimetre on every door; and widths are 2 at 1250 mm, 6 at 864 mm, 4 at 762 mm, and 2 at 813 mm. The ground truth therefore predicted, for DC-W1, 8 pass and 6 fail, with the 864 mm doors passing by 14 mm and the 813 mm doors failing by 37 mm.

**Results.** The evaluation produced 56 verdicts, being 14 doors by 4 rules, as given in Table 11.

**Table 11** Verdict totals for case study B, 14 doors by 4 rules.

| Rule | Pass | Fail | Not applicable | Inconclusive |
|---|---|---|---|---|
| DC-W1, width | 8 | 6 | 0 | 0 |
| DC-W2, clear width property set | 0 | 0 | 0 | 14 |
| DC-M1, measured against declared | 14 | 0 | 0 | 0 |
| DC-Z1, zone, Level 1 only | 4 | 2 | 8 | 0 |
| Total | 26 | 8 | 8 | 14 |

Four observations follow from Table 11. DC-W1 matches the ground truth exactly, door by door. All four verdict categories occur, each for a real reason: DC-W2 is inconclusive on every door because the model's authors never wrote `Pset_DoorCommon.ClearWidth`, and the storey filter of DC-Z1 marks the 8 Level 2 doors not applicable. DC-Z1 found two Level 1 doors with a furnishing element inside the manoeuvring zone, a condition which was not staged and which the model contains. And every record carries the `GlobalId`, the rule identifier, the citation, and the evidence values, namely the widths read, the zone bounds, and the obstructing element.

**Determinism.** The evaluation runs twice from scratch in the test suite and the SHA-256 of the verdict CSV is asserted identical. An independent re-run in a fresh process on the following day gave the same hash. Timestamps are kept in a separate run log and never in the hashed output.

**Override.** A failing 762 mm door receives an `Ara3D_Compliance` property set carrying `Verdict`, `OverrideVerdict`, `OverrideReason`, and `ReviewedBy`, appended to a copy of the model with the byte-exact writer. The test asserts three things: that the entity diff lists exactly the added entities and nothing else; that removing them restores the source file byte for byte; and that the source model is never modified.

```csharp
File.WriteAllBytes(overriddenPath, IfcPatcher.Append(original, builder.Lines));

using var overridden = IfcSourceFile.Load(overriddenPath);
var diff = IfcDiff.Compare(original, overridden);
Assert.That(diff.Added, Is.EqualTo(builder.Ids));
Assert.That(diff.Deleted, Is.Empty);
Assert.That(diff.Changed, Is.Empty);

var restored = IfcPatcher.Remove(overridden, diff.Added);
Assert.That(restored, Is.EqualTo(File.ReadAllBytes(TestPaths.DuplexIfc)));
```

**Test run.** Seven tests passed, in approximately four seconds, on Windows 11 with .NET 8.0.28, verified twice: once by the implementing agent and once in a fresh session.

## 8.4 What the two studies show together

Case study B exercises every part of the recommended architecture except the language model: values read from the file, a rule expressed as data, verdicts keyed by `GlobalId` with evidence, results written back byte-exactly, and reproducibility established by hash. Case study A places the language model in front of the same tools.

Overall, the studies were deliberately built on one model, one writer, and one table shape, so that a verdict and a carbon value are the same kind of object, namely a row keyed by `GlobalId` which may be coloured, summed, asked about, and written back.
