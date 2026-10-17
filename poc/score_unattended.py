"""Score unattended language-model runs of the paper's nine questions against the expected answers.

Usage: python poc/score_unattended.py <results.json> [<results.json> ...] [--markdown <out.md>]

Each results file is the JSON `bimopenmcp-ifc-ask --results` writes: a list of eight (version 2 of the paper) or nine (version 3) objects with
`question`, `answer`, `turns`, `inputTokens`, `outputTokens`, and `toolCalls`. The expected
answers are poc/results/expected_answers.json. The verdicts are:

  Match       the answer states the expected numbers (within 0.1 %) and the expected conclusion
  Partial     the expected numbers are there but so is something wrong, such as container rows
              counted as elements
  Miss        a confidently wrong value, or the expected value absent
  Unanswered  the run recorded an error or hit its turn limit

The comparator is deterministic and reads only the answer text. It settles the numeric
questions; Q2 (which storey is higher) and Q7 (an absence) also look for the expected words, and
their verdicts should be confirmed by reading the transcript.

Q4, Q5 and Q7 were reworded for version 3 and Q9 (the zone) was added. A run of the 2026-10-04 set
carries the old wording of Q4, Q5 and Q7 in its `question` field; those three keep their old rules
(LEGACY below) so the committed table of that set stays reproducible. Everything else is read from
poc/results/expected_answers.json. The score table it prints names
every rule, so a reader can see what "Match" meant for each question. Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = HERE / "results" / "expected_answers.json"

NUMBER = re.compile(r"(?<![\w.])-?\d{1,3}(?:[,  ]\d{3})+(?:\.\d+)?|(?<![\w.])-?\d+(?:\.\d+)?")
ABSENCE = re.compile(
    r"not available|no (?:embodied[- ]carbon )?(?:value|property set|pset|set|data|embodied)|"
    r"does not (?:carry|have|contain)|has no|carries no|is not recorded|no Pset_NRCEmbodiedCarbon|"
    r"not (?:been )?(?:written|recorded|assigned|present)|absent|unavailable|missing",
    re.IGNORECASE)
CONTAINER = re.compile(r"IFCBUILDING(?:STOREY)?|IfcBuilding(?:Storey)?|\bstorey rows?\b|\bbuilding row\b")
LEVEL2_HIGHER = re.compile(
    r"Level 2[^.]{0,80}\b(?:higher|greater|larger|more|highest)\b|\b(?:higher|greater|larger)\b[^.]{0,60}Level 2|"
    r"^\W*\**Level 2\**(?:\s|[.,:])", re.IGNORECASE | re.MULTILINE)
LEVEL1_HIGHER = re.compile(
    r"Level 1[^.]{0,80}\b(?:higher|greater|larger|more|highest)\b|\b(?:higher|greater|larger)\b[^.]{0,60}Level 1|"
    r"^\W*\**Level 1\**(?:\s|[.,:])", re.IGNORECASE | re.MULTILINE)

# Per-class totals the recorded hand-driven session grouped by (paper section 6.1); accepted for
# Q5 beside the analytics-category totals, because the IFC file carries no Category property.
PER_CLASS_Q5 = [17547.4, 5816.9, 5766.3]


# Version 2 wording of the three reworded questions, recognised from the run's own `question` text.
LEGACY = {
    "Q4": "door named",
    "Q5": "in each category",
    "Q7": "embodied carbon of the roof",
}
# Version 2 Q5: the three largest analytics-category totals (Wall, Floor, Other).
LEGACY_Q5_BY_CATEGORY = [22854.1, 5593.5, 4313.1]
GLOBAL_ID = re.compile(r"(?<![\w$])[0-9A-Za-z_$]{22}(?![\w$])")
ZONE_NAME = re.compile(r"Unit\s*B\W{0,4}Level\s*1", re.IGNORECASE)


def numbers(text: str) -> list[float]:
    out = []
    for m in NUMBER.finditer(text):
        raw = m.group(0).replace(",", "").replace(" ", "").replace(" ", "")
        try:
            out.append(float(raw))
        except ValueError:
            pass
    return out


def has(text_numbers: list[float], value: float, rel: float = 0.001, abs_tol: float = 0.051) -> bool:
    return any(abs(n - value) <= max(abs_tol, abs(value) * rel) for n in text_numbers)


def has_all(text_numbers: list[float], values: list[float]) -> bool:
    return all(has(text_numbers, v) for v in values)


@dataclass(frozen=True)
class Verdict:
    question: str
    verdict: str
    rule: str


def unanswered(answer: str) -> bool:
    a = answer.strip()
    return a.startswith("Not answered") or "turn limit" in a.lower() and len(numbers(a)) == 0


def score_q1(a: str, exp: dict) -> Verdict:
    ok = has(numbers(a), exp["answer"])
    return Verdict("Q1", "Match" if ok else "Miss", f"states {exp['answer']}")


def score_q2(a: str, exp: dict) -> Verdict:
    ns = numbers(a)
    means = has(ns, exp["answer"]["Level 2"]) and has(ns, exp["answer"]["Level 1"])
    l2, l1 = bool(LEVEL2_HIGHER.search(a)), bool(LEVEL1_HIGHER.search(a))
    if means and l2 and not l1:
        v = "Match"
    elif l1 and not l2:
        v = "Miss"
    elif means:
        v = "Partial"
    else:
        v = "Miss"
    return Verdict("Q2", v, "Level 2 named higher, means 40.56 and 40.50 stated")


def score_q3(a: str, exp: dict) -> Verdict:
    ns = numbers(a)
    values = [row["value"] for row in exp["answer"]]
    if has_all(ns, values):
        v = "Partial" if (has(ns, 37196.2) and CONTAINER.search(a)) else "Match"
    else:
        v = "Miss"
    return Verdict("Q3", v, "the five values 412.0, 410.8, 402.0, 399.7, 398.6; no container ranked")


def score_q4(a: str, exp: dict) -> Verdict:
    ok = has(numbers(a), exp["answer"]["value"])
    return Verdict("Q4", "Match" if ok else "Miss", "54.0 stated for the door with the given GlobalId")


def score_q4_legacy(a: str, exp: dict) -> Verdict:
    ok = has(numbers(a), exp["answer"]["value"])
    return Verdict("Q4", "Match" if ok else "Miss", "54.0 stated (four doors share the name; listing all four is a match)")


def score_q5(a: str, exp: dict) -> Verdict:
    ns = numbers(a)
    if has_all(ns, list(exp["answer"].values())):
        v = "Partial" if CONTAINER.search(a) else "Match"
    else:
        v = "Miss"
    return Verdict("Q5", v, "all 14 per-class totals stated; container rows not listed")


def score_q5_legacy(a: str, exp: dict) -> Verdict:
    ns = numbers(a)
    by_category = sum(has(ns, v) for v in LEGACY_Q5_BY_CATEGORY) >= 3
    by_class = sum(has(ns, v) for v in PER_CLASS_Q5) >= 3
    if by_category or by_class:
        v = "Partial" if CONTAINER.search(a) else "Match"
    else:
        v = "Miss"
    return Verdict("Q5", v, "top three totals by analytics category or by IFC class; container rows not listed")


def score_q6(a: str, exp: dict) -> Verdict:
    ok = exp["answer"]["AnalysisRunId"] in a and "2026-09-17" in a
    return Verdict("Q6", "Match" if ok else "Miss", "run-2026-09-17-01 and 2026-09-17 stated")


def score_q7(a: str, exp: dict) -> Verdict:
    wanted = exp["answer"][0]["GlobalId"]
    ids = set(GLOBAL_ID.findall(a))
    named = wanted in ids or re.search(r"\bIFCROOF\b", a, re.IGNORECASE) is not None
    others = {i for i in ids if i != wanted and any(c.isdigit() for c in i) and any(c.isalpha() for c in i)}
    if named and not others:
        v = "Match"
    elif named:
        v = "Partial"
    else:
        v = "Miss"
    return Verdict("Q7", v, "the one IfcRoof (0jf0rYHfX3RAB3bSIRjmxl) named, no other element listed")


def score_q7_legacy(a: str, exp: dict) -> Verdict:
    absence = bool(ABSENCE.search(a))
    leads_with_absence = a.strip().lower().startswith("not available")
    big = [n for n in numbers(a) if n > 100 and n not in (2026,)]
    if absence and (leads_with_absence or not big):
        v = "Match"
    elif absence:
        v = "Partial"
    else:
        v = "Miss"
    return Verdict("Q7", v, "absence stated first; an embodied value given as the answer is a Miss")


def score_q8(a: str, exp: dict) -> Verdict:
    ns = numbers(a)
    values = list(exp["answer"].values())
    if has_all(ns, values):
        v = "Match"
    elif has_all(ns, [v * 2 for v in values]):
        v = "Miss"
    else:
        v = "Miss"
    return Verdict("Q8", v, "49,451.2; 48,696.8; 11,761.3; 5,821.0 stated (doubles are the aggregate defect)")


def score_q9(a: str, exp: dict) -> Verdict:
    name = ZONE_NAME.search(a) is not None
    value = has(numbers(a), exp["answer"]["value"])
    v = "Match" if name and value else "Partial" if name or value else "Miss"
    return Verdict("Q9", v, "Unit B Level 1 named with 78.04 kWh/m2/yr")


SCORERS = [score_q1, score_q2, score_q3, score_q4, score_q5, score_q6, score_q7, score_q8, score_q9]
LEGACY_SCORERS = {"Q4": score_q4_legacy, "Q5": score_q5_legacy, "Q7": score_q7_legacy}


def score_run(results: list[dict], expected: dict) -> list[Verdict]:
    out = []
    for i, (item, scorer) in enumerate(zip(results, SCORERS), 1):
        key = f"Q{i}"
        answer = item.get("answer") or ""
        if unanswered(answer):
            out.append(Verdict(key, "Unanswered", "error or turn limit"))
        else:
            legacy = LEGACY.get(key)
            if legacy and legacy in item.get("question", ""):
                scorer = LEGACY_SCORERS[key]
            out.append(scorer(answer, expected[key]))
    return out


def tokens(results: list[dict]) -> tuple[int, int, int]:
    return (sum(r.get("turns", 0) for r in results),
            sum(r.get("inputTokens", 0) for r in results),
            sum(r.get("outputTokens", 0) for r in results))


def markdown(runs: dict[str, list[Verdict]], results_by_run: dict[str, list[dict]]) -> str:
    names = list(runs)
    lines = ["| # | Rule | " + " | ".join(names) + " | Matches |", "|---|---|" + "---|" * (len(names) + 1)]
    for i in range(max(len(v) for v in runs.values())):
        key = f"Q{i + 1}"
        row = [runs[n][i].verdict for n in names]
        rule = runs[names[0]][i].rule
        lines.append(f"| {key} | {rule} | " + " | ".join(row) + f" | {row.count('Match')} of {len(names)} |")
    totals = [str(sum(1 for v in runs[n] if v.verdict == "Match")) for n in names]
    lines.append("| **Matches** | | " + " | ".join(totals) + " | |")
    lines.append("")
    lines.append("| Run | Turns | Input tokens | Output tokens |")
    lines.append("|---|---|---|---|")
    for n in names:
        t, i, o = tokens(results_by_run[n])
        lines.append(f"| {n} | {t} | {i:,} | {o:,} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    out_md = None
    if "--markdown" in argv:
        k = argv.index("--markdown")
        out_md = Path(argv[k + 1])
        argv = argv[:k] + argv[k + 2:]
    files = [Path(a) for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    runs, results_by_run = {}, {}
    for f in files:
        results = json.loads(f.read_text(encoding="utf-8"))
        runs[f.stem] = score_run(results, expected)
        results_by_run[f.stem] = results
    text = markdown(runs, results_by_run)
    print(text)
    if out_md:
        out_md.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
