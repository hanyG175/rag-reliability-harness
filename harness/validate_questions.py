import json
import sys
from collections import Counter

TYPES = {"answerable", "unanswerable", "false_premise", "out_of_scope"}
REQUIRED = {"id", "type", "question", "expected_answer", "source_passage_id"}
NEEDS_SOURCE = {"answerable", "false_premise"}
NEEDS_NO_SOURCE = {"unanswerable", "out_of_scope"}


def validate(path):
    errors, ids, counts, questions = [], set(), Counter(), set()
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {n}: invalid JSON ({e.msg})")
                continue
            missing = REQUIRED - row.keys()
            if missing:
                errors.append(f"line {n}: missing fields {sorted(missing)}")
                continue
            if row["type"] not in TYPES:
                errors.append(f"line {n}: unknown type {row['type']!r}")
                continue
            counts[row["type"]] += 1
            if row["id"] in ids:
                errors.append(f"line {n}: duplicate id {row['id']!r}")
            ids.add(row["id"])
            q = (row["question"] or "").strip()
            if not q:
                errors.append(f"line {n}: empty question")
            elif q.lower() in questions:
                errors.append(f"line {n}: duplicate question text")
            questions.add(q.lower())
            has_source = bool(row["source_passage_id"])
            if row["type"] in NEEDS_SOURCE and not has_source:
                errors.append(f"line {n}: {row['type']} needs source_passage_id")
            if row["type"] in NEEDS_NO_SOURCE and has_source:
                errors.append(f"line {n}: {row['type']} must not have source_passage_id")
            if row["type"] in NEEDS_SOURCE and not row["expected_answer"]:
                errors.append(f"line {n}: {row['type']} needs expected_answer")
    return errors, counts


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    errors, counts = validate(sys.argv[1])
    total = sum(counts.values())
    print(f"{total} questions: " + ", ".join(f"{t}={counts[t]}" for t in sorted(TYPES)))
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} problem(s) found")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
