# Autoresearch Runner

This repo now includes a real unattended loop runner:

```bash
cd /Users/joy/autoresearch/skill-lab/market-research
python3 scripts/run_autoresearch.py --iterations 10
```

## What it does

Each iteration:
1. snapshots `source/SKILL.md`
2. writes iteration context to `runs/autoresearch_loop/<run_id>/iteration_<n>/context.json`
3. runs a mutator command
4. runs `scripts/evaluate_skill.py`
5. keeps or reverts the candidate
6. appends the outcome to `results.tsv`

## Default behavior

- Target artifact: `source/SKILL.md`
- Evaluator: `python3 scripts/evaluate_skill.py`
- Validation context: `python3 scripts/summarize_validation.py`
- Default mutator: `python3 scripts/heuristic_mutator.py ...`
- Keep rule: only keep candidates that improve the evaluator score

This is intentionally conservative. It prevents the loop from drifting when the evaluator is already saturated.

## Why this is not yet a 100-iteration creative loop

The orchestration is now real, but the default mutator is deliberately narrow.

That is by design:
- the evaluator is good enough to block regressions
- it is not yet good enough to let a free-form generator rewrite the skill indefinitely without overfitting

If you want the kind of long unattended runs people talk about, swap in a stronger mutator command.

## Plugging in a stronger mutator

The runner passes context through environment variables:

- `AUTORESEARCH_ROOT`
- `AUTORESEARCH_TARGET`
- `AUTORESEARCH_CONTEXT`
- `AUTORESEARCH_MUTATOR_STATE`
- `AUTORESEARCH_ITERATION_DIR`

You can replace the default mutator with any command that edits `AUTORESEARCH_TARGET` in place and prints a final JSON line like:

```json
{"changed": true, "strategy": "llm_patch", "note": "added stricter evidence rule"}
```

Example:

```bash
python3 scripts/run_autoresearch.py \
  --mutator-command 'python3 scripts/my_llm_mutator.py --target "$AUTORESEARCH_TARGET" --context "$AUTORESEARCH_CONTEXT"'
```

## Safe operating modes

Dry run:

```bash
python3 scripts/run_autoresearch.py --dry-run
```

Stop early after repeated non-improvements:

```bash
python3 scripts/run_autoresearch.py --iterations 25 --stop-after-no-improvement 5
```

Allow equal-score keeps only when you trust the evaluator:

```bash
python3 scripts/run_autoresearch.py --keep-on-equal
```

## Current recommendation

Use the default runner now for:
- safe orchestration
- reproducible keep/revert behavior
- artifact logging

Do not run it for hours with `--keep-on-equal` until the evaluator learns to score real-request reruns more directly.
