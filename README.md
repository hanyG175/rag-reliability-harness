# RAG Reliability Harness

An open test harness that checks whether a RAG (retrieval-augmented generation) system
answers correctly, stays grounded in its sources, and refuses when it should.

**Status: just started (20 Nov 2026). No results yet.** This README is the plan, and the
checklist below is updated as each step is actually finished.

## Why

RAG systems fail in quiet ways: they invent answers when the documents do not contain
them, accept false assumptions in the question, or refuse questions they could have
answered. This project measures those failures instead of guessing at them.

## Planned test set (about 100 questions)

| Type | Planned count | A good system |
| --- | --- | --- |
| Answerable | 40 | Answers correctly and cites the source passage |
| Unanswerable | 20 | Says the corpus does not contain the answer |
| False premise | 20 | Corrects the wrong assumption |
| Out of scope | 20 | Declines politely |

Each question is stored as one JSON line (see `data/test_questions.example.jsonl`).
The example file only shows the format. It is not the real test set.

## Planned metrics

- Retrieval: hit rate at k and MRR
- Groundedness: whether every claim in the answer is supported by the retrieved text
- Refusal: precision and recall of "should refuse" versus "did refuse"
- LLM-as-judge, checked against 30 answers graded by hand

## Roadmap

- [x] Create the repo and write the plan
- [x] Test file format and validator (`harness/validate_questions.py`)
- [ ] Baseline RAG system over a small corpus
- [ ] Ingestion pipeline (clean, deduplicate, chunk, metadata, quality checks)
- [ ] 100 reviewed test questions
- [ ] Automatic scoring
- [ ] Compare three setups and write a failure analysis
- [ ] Publish the dataset and a write-up

## Check a test file

```bash
python harness/validate_questions.py data/test_questions.example.jsonl
```

## Repo layout

```
data/       test questions (JSONL)
harness/    scripts
```

## Author

Hani Gaouaou. Built with AI coding assistance where noted in commit messages.
