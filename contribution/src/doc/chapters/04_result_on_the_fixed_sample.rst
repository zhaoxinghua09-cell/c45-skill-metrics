

.. _chapter04:

Result on the fixed sample
==========================

Twelve skills, one root directory, one date (2026-11-17). Aggregate scores ranged from 62 to 76 with a mean
of 69.3; five of the twelve fell below the 70-point threshold, and the tool's exit code distinguished those
five from the rest.

The finding worth reporting is not the mean but the variance structure. Purpose and behavioural returned
5.0 for all twelve: every item in the sample states an action and an object, and every item states what it
does. Two dimensions that never vary are not measurements of this population — they are constants, and they
inflate the aggregate by contributing a fixed maximum. Usage returned 2.0 for all twelve, which is not a
constant by design but a ceiling imposed by the sample: none of the twelve documents its invocation in the
form the rule rewards.

Effective discrimination therefore came from three dimensions: fields, conciseness and context. That is a
narrower instrument than the six-dimension label suggests, and a group adopting such a score should say so.

Re-run: the public package is https://github.com/zhaoxinghua09-cell/c45-skill-metrics (DataTracker FG-TIDA-WG0-004, version 0.4). From the repository root, run: .\preview.ps1 . Expected output: the documents are served at http://127.0.0.1:8000, and the result reported above is reproduced: aggregate scores from 62 to 76 with a mean of 69.3, five of the twelve below the 70-point threshold.
