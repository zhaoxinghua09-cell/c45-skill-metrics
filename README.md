# A.4.5 - Metrics for an Agent Skill Ecosystem

Input document for ITU-T FG-TIDA work item **A.4.5**: a six-dimension score applied to
twelve agent skills on a fixed date, and the one conclusion the result supports - that a
metric is useful only where it discriminates, so a metric offered to the group should
carry its distribution rather than its mean.

**Status:** submitted to the FG-TIDA secretariat on 28 November 2026 as an input document
for the 1st in-person meeting (Paris, 30 November - 1 December 2026), in Word form.
Offered for discussion; not adopted, not a settled position, and not an ITU-T
Recommendation.

## Contents

| File | What it is |
|---|---|
| `contribution/src/doc/index.rst` | the input document as a reStructuredText package in the FG-TIDA template layout (entry document; chapters under `chapters/`) |
| `contribution/src/doc/chapters/` | the eight chapters, in order: the six dimensions, the result on the fixed sample, what follows for A.4.5 |
| `contribution/src/doc/yaml/example.yaml` | the worked example the note refers to |
| `contribution/README.md` | how the template package is laid out, and how to render it |

## Read it

`.rst` is plain text: any editor opens it. To render the package as a page, the template's
own instructions apply (`contribution/requirements.txt`, `contribution/preview.ps1`); no
network access is needed for the text itself.

## What is not claimed

Twelve skills on one date is a sample, not a population. Two of the six dimensions
returned the same value for every item in this sample, which is a statement about the
sample and the dimensions as worded - not a claim that those dimensions are useless in
general.

## Run the score

One command, offline, no dependencies, deterministic, under one second:

```bash
python demo/score_demo.py              # three-item fixture
python demo/score_demo.py <directory>  # your own skill tree
```

It prints the per-item table, the per-dimension mean and range, the aggregate distribution, and
names any dimension that is constant over the sample. The fixture is three items, not the twelve of
2026-11-17, so it does not claim to reproduce the mean of 69.3; what it reproduces is the rule set.

## Contact

Xinghua Zhao (Steven Zhao), independent researcher, ORCID iD 0009-0001-0512-1237,
individual capacity, no organisation represented - zhaoxinghua06@126.com
