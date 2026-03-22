# Market Research Skill Autoresearch Program

Goal: improve the market research skill so it is internally consistent, actionable, and reliable for repeated product and market research tasks.

## Current phase
- `source/SKILL.md` is frozen.
- Do not edit the skill again unless real-request validation exposes a concrete, repeatable defect.
- Use `/Users/joy/autoresearch/skill-lab/market-research/docs/validation_workflow.md` for the next phase.

## Mutable artifact
- /Users/joy/autoresearch/skill-lab/market-research/source/SKILL.md

## Companion references
- /Users/joy/autoresearch/skill-lab/market-research/source/data-sources.md
- /Users/joy/autoresearch/skill-lab/market-research/source/research-prompts.md

## Hard checks
- All referenced local files in `SKILL.md` must exist at the paths the skill names.
- The skill must define when to use it, how to choose modes, and what to output.
- The skill must distinguish verified facts, estimates, and speculation.
- The evaluator score must not regress.

## Scoring priorities
1. instruction completeness
2. internal consistency
3. reference integrity
4. output contract clarity
5. evaluation coverage

## Loop
1. inspect the current `SKILL.md`
2. run the evaluator
3. make one focused improvement
4. re-run the evaluator
5. keep only if the score improves or a concrete defect is removed
6. log the result in `results.tsv`
