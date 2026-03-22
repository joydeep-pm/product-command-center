# Skill Workflow

Use this lab to improve the market research skill with a controlled loop.

## Current status
- The synthetic autoresearch loop is complete for now.
- `/Users/joy/autoresearch/skill-lab/market-research/source/SKILL.md` is frozen pending real-request failures.
- Use `/Users/joy/autoresearch/skill-lab/market-research/docs/validation_workflow.md` to validate the frozen skill against real prompts before reopening edits.

## Mutable file
- `/Users/joy/autoresearch/skill-lab/market-research/source/SKILL.md`

## Run baseline
```bash
cd /Users/joy/autoresearch/skill-lab/market-research
python3 scripts/evaluate_skill.py
```

## Iterate
1. Make one focused change in `source/SKILL.md`
2. Re-run `python3 scripts/evaluate_skill.py`
3. Log the result in `results.tsv`
4. Keep only changes that improve the score or remove a concrete defect

## First obvious defect
- `SKILL.md` currently references `references/research-prompts.md` and `references/data-sources.md`
- those files actually live beside `SKILL.md`
- the first iteration should fix those paths
