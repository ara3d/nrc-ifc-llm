# 7 The large language model and agent layer

This section addresses the third objective of the statement of work, namely how to build a layer in which a person asks a question in plain language and receives a correct answer about an enriched model. The design follows from one observation concerning what language models are and are not able to do well.

## 7.1 Why the model is not given the file

An IFC file is a serialisation of an object graph. A question such as "what is the total operational carbon on Level 2" requires finding the storey entity, following the containment relationship to its elements, finding each element's property set relationship, finding the set, finding the property, reading the value, and summing. In a file of 38,898 entities the relevant entities are scattered, and the file is far larger than any model's context window. Even where a file does fit, a language model reading STEP text performs arithmetic by pattern matching and produces plausible rather than correct totals.

The alternative is to give the model tools. A tool is a function with a typed signature that the model may call, which the runtime executes, returning the result. The model then reasons over results that are small, structured, and correct. This is the design of every practical IFC MCP server surveyed [24], and the design adopted here; the difference lies in what the tools are.

## 7.2 Design principles

Four principles were applied. Each was derived from running varied questions against the implementation and reading the transcripts, and the toolkit's demonstration notes [33] record the failures that motivated them.

**Few, typed, read-only tools.** A server that exposes the whole IFC API as 200 tools gives the model too many ways in which to be wrong. The implementation exposes 29 tools grouped by question shape, as listed in Annex C. Every SQL tool accepts one read-only statement; `DROP`, `INSERT`, and statement chaining are rejected, and the rejection is tested.

**A columnar copy rather than the object graph.** The IFC file is converted once per session to BIM Open Schema and loaded into DuckDB. Questions then become SQL over tables with text views, which a model writes reliably. The conversion is the expensive step and is performed once rather than once per question.

**Questions run in the opposite direction.** The per-element tools, which answer "what does element N carry", are the wrong shape for almost every real question, such as "which elements are load bearing" or "`Height` for all the windows". An inverted parameter index, built once per session, answers those in a single call. Without it, the model made one call per element.

**Answers carry their derivation.** Every list result reports its unpaged total, so that the model is able to distinguish a complete answer from a truncated one. In the dataflow surface, a question becomes a graph, the graph is evaluated, and a run record pins the graph hash and every input by content hash. A number therefore arrives with a means of recomputing it.

## 7.3 The tool surface

The IFC MCP server has three groups of tools. The data tools answer questions about entities, attributes, properties, quantities, relations, and the spatial tree directly from the parsed file, without loading geometry. The geometry tools answer questions about meshes, bounds, and volumes. The analytics tools convert the model to BOS, list the tables, run read-only SQL, and export results. Annex C gives the full surface.

A representative exchange is shown below, with the model's tool calls as they appear in a transcript. The numbers in this exchange are illustrative of the shape of an answer rather than measured results; Section 8.2 reports the recorded run.

```text
User:  Which storeys have the most operational carbon, and what is the total for each?

Agent: ifc_to_bos { path: "duplex.ifc" }
       -> { tables: 9, entities: 38898 }

Agent: ifc_sql { sql: "SELECT p.Value AS storey ... " }
       (reads the ContainedIn relations and the Pset_NRCOperationalCarbon values)

Agent: ifc_sql { sql:
         "SELECT storey, round(sum(oc), 1) AS total_kgCO2e_per_year, count(*) AS elements
            FROM element_carbon GROUP BY storey ORDER BY total DESC" }
       -> { total: 2, rows: [["Level 2", 12406.3, 141], ["Level 1", 11874.9, 127]] }

Agent: Level 2 has the higher total at 12,406 kgCO2e per year across 141 elements;
       Level 1 has 11,875 across 127. Values come from Pset_NRCOperationalCarbon
       on each element, run id run-2026-07-14-01.
```

## 7.4 The dataflow surface

The second surface is the BimOpenFlow MCP server, whose tools are the same operations that back the web editor: `describeDatabase`, `getNodeCatalog`, `editGraph`, `evaluate`, `getResult`, and `createRun`. A question becomes a graph of small nodes rather than one SQL string, and the graph persists in a store in which a person is able to open it, inspect each intermediate table, and edit it.

This arrangement matters for three reasons. The person who asked the question is able to see how the answer was constructed. The next question, such as "now only the doors", is an edit to the same graph. And the graph that colours the model, described in Section 6.2, and the graph that answers the question are the same kind of object, so that "colour Level 2 by the values just summed" is one further node.

Nine tactics were required to make this work on small and large models alike, of which four matter most. The first is a schema summary that the model is able to afford to read, with companion columns folded and empty tables given only a name and a count. The second is a node guide in the system prompt, covering the expression language, the aggregate syntax, and the fact that `sql.query` exists for anything the table nodes cannot express. The third is a single call to build a graph; applying a list of edits at once and saving once reduced input tokens per request from between 2 and 4 million to between 100 and 300 thousand. The fourth is a check performed by the host after the model reports completion, verifying that every node evaluated, that an `answer` node is present, and that its table has rows; an empty answer is reported back with the row count of every upstream node, and the model is given two further turns in which to correct it or to state honestly why the answer is empty.

On the toolkit's Snowdon Towers test database, twelve requests concerning rooms, roofs, storeys, doors, and lineage produced ten correct graphs, one honest answer without a graph, and one correctly empty graph with an explanation on a small model, and eleven correct graphs and one honest answer on a mid-sized one. Where a hand-built graph existed for the same question, the counts matched. It should be noted that these figures were obtained on the toolkit's own test database rather than on carbon and energy questions over an enriched IFC, a limitation stated in Section 9.3.

## 7.5 Compliance expressed as a query

A code-compliance rule is a query with a verdict column, and the compliance node pack expresses this directly. A `check.rule` node takes a table of element rows and a Boolean expression, and appends four columns: `verdict`, `checkId`, `checkTitle`, and `citation`. A true expression yields `Pass`; a false expression yields `Fail`, or `NeedsReview` where a second expression says so; and a null result, signifying that the fact required was absent, yields `InfoNotAvailable`. Absence is reported and never skipped.

```csharp
verdicts[i] = expr.Eval(lookup) switch
{
    null => Verdict.InfoNotAvailable,
    BooleanScalar { Value: true } => Verdict.Pass,
    _ => review?.Eval(lookup) is BooleanScalar { Value: true } ? Verdict.NeedsReview : Verdict.Fail,
};
```

The verdict table is an ordinary table. It may be coloured onto the model, summed per storey, exported, or written back into the IFC as a property set. Section 8.3 reports a checker built on the same four-verdict scheme running over real doors.

## 7.6 Recommendation in brief

In summary, it is recommended that six measures be adopted for the query layer:

1. The language model should be placed behind a small, typed, read-only tool surface, and should not be given the file;
2. The IFC should be converted once to a columnar form, and questions answered with SQL over text views;
3. Inverted parameter tools should be provided, so that "which elements have X" is a single call;
4. Every answer should carry its derivation, by totals on lists and by graphs and run records for dataflow questions;
5. Compliance checks should be treated as queries with a verdict column, and missing data should be required to produce an explicit verdict rather than a silent pass;
6. MCP should be used, so that one server serves a chat client, a custom agent, and the web editor alike.
