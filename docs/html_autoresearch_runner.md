# HTML Autoresearch Runner

This is a bounded unattended loop for `/Users/joy/autoresearch/app/dashboard.html`.

## Purpose

- mutate the dashboard conservatively
- run the evaluator after each change
- keep only score-improving changes
- stop when there is no higher move left

## Entry Points

- Runner: `/Users/joy/autoresearch/scripts/run_dashboard_autoresearch.py`
- Mutator: `/Users/joy/autoresearch/scripts/html_heuristic_mutator.py`
- Evaluator: `/Users/joy/autoresearch/scripts/evaluate_dashboard.py`

## Current Heuristic Strategies

1. Add `Revenue Unlock by Quarter`
2. Add `Delivery Confidence`

These strategies are deterministic and string-anchored. They are intentionally narrow so the loop does not drift into free-form rewrites.

## How To Run

```bash
cd /Users/joy/autoresearch
python3 scripts/run_dashboard_autoresearch.py --iterations 4
```

Dry run:

```bash
python3 scripts/run_dashboard_autoresearch.py --dry-run
```

## Safety Model

- The runner snapshots the HTML before each mutation.
- It reverts any non-improving iteration automatically.
- It appends every iteration result to `/Users/joy/autoresearch/results.tsv`.
- It stores per-run artifacts under `/Users/joy/autoresearch/runs/html_autoresearch/`.

## Verification Standard

The evaluator is necessary but not sufficient.

After a kept run, verify:

1. the page loads over HTTP
2. console errors are `0`
3. the new metrics render with live source-backed data
4. the overview still works on a narrow viewport

## What Needs To Be True For 95% Confidence

To let the loop add higher-value PM metrics safely, the next missing inputs are:

1. canonical RAG thresholds approved by product leadership
2. a trusted mapping from EPICs to owning team / owner
3. quarter-level revenue attribution that leadership agrees is decision-grade
4. explicit definitions for `blocked`, `at risk`, and `sellable`

Without those, the loop can still improve the dashboard, but some future metrics will remain heuristic rather than governance-grade.
