# Product Command Center Program

This repo adapts the autoresearch loop to a stakeholder-facing product command center.

## Objective

Continuously improve `/Users/joy/autoresearch/app/dashboard.html` so business stakeholders can understand the product portfolio, roadmap, performance, risks, dependencies, and strategic rationale to a granular level.

## Mutable file

- `/Users/joy/autoresearch/app/dashboard.html`

## Fixed source-of-truth inputs

- `/Users/joy/autoresearch/data/command_center_data.json`
- `/Users/joy/autoresearch/docs/source_brief.md`
- `/Users/joy/autoresearch/scripts/extract_sources.py`
- `/Users/joy/autoresearch/scripts/evaluate_dashboard.py`

## Non-negotiable requirements

1. The dashboard must be useful to business stakeholders, not just aesthetically polished.
2. Every iteration must preserve or improve content coverage of:
   - executive snapshot
   - strategic imperatives
   - quarterly roadmap
   - epic register
   - loss intelligence
   - competitive parity
   - compliance and risk
   - market expansion bets
   - resource and capacity plan
   - dependencies and operating constraints
3. Prefer simple, legible changes over ornamental complexity.
4. Never invent product facts that are not grounded in the source files.

## Evaluation loop

1. Refresh source artifacts with `python3 scripts/extract_sources.py` if inputs changed.
2. Make one focused improvement in `app/dashboard.html`.
3. Run `python3 scripts/evaluate_dashboard.py`.
4. Log the result in `results.tsv`.
5. Keep only improvements that raise stakeholder usefulness without breaking rendering.

## Scoring philosophy

The dashboard is scored on a 100-point rubric:

- 35 points: content coverage
- 25 points: decision-support clarity
- 15 points: strategic traceability to source docs
- 15 points: information architecture and navigation
- 10 points: visual/render integrity

A change that looks better but hides product truth is a regression.
