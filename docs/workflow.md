# Workflow

## Purpose

This repo uses an autoresearch-style loop to improve a business-facing product command center, not just a visual dashboard.

## Step-by-step loop

1. Refresh the structured source artifacts.
   - `python3 scripts/extract_sources.py`
2. Evaluate the current dashboard.
   - `python3 scripts/evaluate_dashboard.py`
3. Review `docs/source_brief.md` and choose one focused improvement.
4. Edit `/Users/joy/autoresearch/app/dashboard.html`.
5. Re-run the evaluator.
6. Log the result in `results.tsv`.
7. Keep only changes that improve stakeholder usefulness and preserve render integrity.

## Source hierarchy

1. Workbook: authoritative structured roadmap and operating data.
2. Strategy PDFs: executive framing, strategic rationale, ROI logic, hiring constraints.
3. HTML: presentation layer for business stakeholders.

## Recommended first improvements

1. Align dashboard navigation to the source model: snapshot, strategy, roadmap, parity, risks, resources.
2. Expose top-loss deals and mapped EPIC recovery actions in a single pane.
3. Add quarter-level strategic themes and dependency warnings.
4. Add a source index so every headline metric can be traced back.
