#!/usr/bin/env python3
"""Six-dimension score, implemented from Chapter 3 of FG-TIDA-WG0-004.

Run:
    python score_demo.py              # built-in fixture, three items
    python score_demo.py <directory>  # your own skill directory

No dependencies, Python 3.8+, offline, deterministic, under one second.

WHAT THIS IS. The instrument as worded in the contribution: six dimensions, each
scored 0-5 by the rules below, aggregated as a weighted blend of mean and minimum so
that one weak dimension cannot be hidden by five strong ones. It prints the per-item
table, the per-dimension mean and range, the aggregate distribution, and names any
dimension that is constant over the sample.

WHAT THIS IS NOT. It is not the twelve-item run of 2026-11-17 and cannot reproduce its
mean of 69.3: that sample's raw per-item values were not retained, and this script
carries a three-item fixture instead. Running on the fixture tells you what the
instrument returns, not what the 2026 sample scored.

ONE APPARENT CONTRADICTION, stated here rather than found by a reader. Chapter 4 records
that Purpose was 5.0 for all twelve items in that sample. On this fixture Purpose is
not constant: the rule as worded gives 2 to an item that names no object. Both are
true - Chapter 4 reports a sample in which every item happened to state an action and
an object, while the rule itself can return less. The constant was a property of the
sample, not of the instrument.
"""
import os, re, statistics, sys, textwrap

DIMENSIONS = ['purpose', 'usage', 'behavioural', 'fields', 'conciseness', 'context']
WEIGHTS = {'purpose': 1, 'usage': 1, 'behavioural': 1, 'fields': 1, 'conciseness': 1, 'context': 1}
MEAN_SHARE, MIN_SHARE = 0.7, 0.3          # the plain reading of "weighted blend of mean and minimum"

FIXTURE = {
'clean-ticket-sorter': """---
name: clean-ticket-sorter
description: Sorts support tickets into queues by urgency and product area.
version: 1.2.0
---
## Usage
```
python sort_tickets.py --inbox ./inbox --out ./queues
```
## Behaviour
Reads every ticket in the inbox, assigns a queue, and writes one file per queue.
Tickets it cannot classify go to manual-review.
## When to use
Use when a backlog has more than 200 unclassified tickets.
Do not use on tickets that contain customer payment details.
""",
'thin-greeter': """---
name: thin-greeter
description: Greets.
---
It greets people. It greets people when they arrive. It greets them when they arrive.
""",
'partial-invoice-reader': """---
name: partial-invoice-reader
description: Extracts totals and dates from invoice PDFs.
---
## Usage
```
python read_invoice.py invoice.pdf
```
## Behaviour
Prints the invoice total and the invoice date. If the PDF is a scan it prints nothing and
returns exit code 2 rather than guessing a total from an empty text layer.
## Context
Applies to digitally generated invoices only; not to scanned images.
""",
}

STOP = re.compile(r'\b(it|the|a|an|of|to|and|is|are|this|that|when|they|them)\b')


def sentence_count(text):
    return max(1, len(re.findall(r'[.!?](\s|$)', text)))


def score_purpose(t):
    """does the artifact state an action and an object"""
    m = re.search(r'description:\s*(.+)', t)
    if not m:
        return 0
    d = m.group(1).strip()
    has_verb = bool(re.search(r'\b(sort|read|extract|greet|parse|scan|write|convert|check|'
                              r'validate|render|summar|classif|fetch|build|generat|greets|sorts|'
                              r'reads|extracts)\w*', d, re.I))
    has_object = bool(re.search(r'\b(tickets?|files?|pdfs?|invoices?|data|text|images?|records?|'
                                r'queues?|people|skills?|manifests?|document\w*)\b', d, re.I))
    return 5 if (has_verb and has_object) else (2 if has_verb or has_object else 0)


def score_usage(t):
    """does it show how the artifact is invoked"""
    if re.search(r'##\s*usage', t, re.I) and re.search(r'```', t):
        return 5 if re.search(r'(python|node|npm|bash|sh)\s', t) else 3
    if re.search(r'`[^`]*--\w+', t):
        return 3
    return 0


def score_behavioural(t):
    """does it state what the artifact does when run"""
    m = re.search(r'##\s*behaviou?r\s*\n+(.+?)(\n##|\Z)', t, re.S | re.I)
    if not m:
        return 0
    body = m.group(1).strip()
    verbs = len(re.findall(r'\b(writes?|reads?|returns?|prints?|assigns?|writes|exits?|raises?|'
                           r'emits?|records?|sends?|fails?)\b', body, re.I))
    return 5 if verbs >= 4 else (3 if verbs >= 2 else 1)


def score_fields(t):
    """are the required fields present and populated"""
    need = ['name', 'description', 'version']
    got = sum(1 for k in need if re.search(rf'^{k}:\s*\S+', t, re.M))
    return [0, 1, 3, 4, 5][got]


def score_conciseness(t):
    """is the text free of repetition and padding"""
    sents = sentence_count(t)
    uniq = len(set(re.findall(r'\b[a-z]{3,}\b', t.lower())))
    ratio = uniq / max(1, len(re.findall(r'\b[a-z]{3,}\b', t.lower())))
    rep = 1 - ratio
    filler = len(STOP.findall(t)) / max(1, sents)
    if rep > 0.35 or filler > 12:
        return 1
    if rep > 0.22 or filler > 9:
        return 3
    return 5


def score_context(t):
    """does it state when the artifact applies and when it does not"""
    applies = bool(re.search(r'(when to use|applies to|use when)', t, re.I))
    excludes = bool(re.search(r"(do not use|not to |does not apply|not for)", t, re.I))
    return 5 if (applies and excludes) else (2 if (applies or excludes) else 0)


SCORERS = {'purpose': score_purpose, 'usage': score_usage, 'behavioural': score_behavioural,
           'fields': score_fields, 'conciseness': score_conciseness, 'context': score_context}


def score(text):
    return {d: SCORERS[d](text) for d in DIMENSIONS}


def aggregate(s):
    vals = [s[d] for d in DIMENSIONS]
    return round(100 * (MEAN_SHARE * (sum(vals) / len(vals)) + MIN_SHARE * min(vals)) / 5, 1)


def collect(path):
    if not path:
        return dict(FIXTURE), 'built-in fixture (3 items) - not the twelve-item sample of 2026-11-17'
    items = {}
    for root, _, files in os.walk(path):
        for f in sorted(files):
            if f.lower().endswith(('.md', '.txt', '.rst')):
                p = os.path.join(root, f)
                try:
                    items[os.path.relpath(p, path)] = open(p, encoding='utf-8', errors='ignore').read()
                except Exception:
                    pass
    return items, path


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    items, label = collect(target)
    if not items:
        print('no .md/.txt/.rst found under', label); return 2

    print('six-dimension score - FG-TIDA-WG0-004, Chapter 3 rules')
    print('sample:', label, '| items:', len(items))
    print()
    print(f"{'item':38} {'purp':>4} {'usag':>4} {'behv':>4} {'flds':>4} {'cncs':>4} {'ctxt':>4} {'agg':>6}")
    rows = {}
    for name, text in items.items():
        s = score(text); rows[name] = s
        print(f"{name[:38]:38} {s['purpose']:>4} {s['usage']:>4} {s['behavioural']:>4} "
              f"{s['fields']:>4} {s['conciseness']:>4} {s['context']:>4} {aggregate(s):>6}")

    aggs = [aggregate(s) for s in rows.values()]
    print()
    print('distribution (aggregate):', ' '.join(f'{a:g}' for a in sorted(aggs)))
    print(f'mean {statistics.mean(aggs):.1f} | min {min(aggs):g} | max {max(aggs):g} | '
          f'below 70: {sum(1 for a in aggs if a < 70)} of {len(aggs)}')

    print()
    print('per dimension, over this sample:')
    constant = []
    for d in DIMENSIONS:
        vals = [s[d] for s in rows.values()]
        lo, hi = min(vals), max(vals)
        tag = 'CONSTANT - carries no discrimination here' if lo == hi else ''
        if lo == hi:
            constant.append(d)
        print(f'  {d:12} mean {statistics.mean(vals):.2f}  range {lo}-{hi}  {tag}')
    if constant:
        print()
        print('Named rather than averaged away:', ', '.join(constant),
              '. A dimension that is constant over a sample reports the sample, not the instrument.')
    print()
    print('exit 0 - the run is reproducible: same fixture, same numbers.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
