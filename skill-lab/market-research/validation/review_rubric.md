# Review Rubric

Score each real request on a 0-2 scale.
- `0`: failed badly
- `1`: partially correct or uneven
- `2`: strong

## Dimensions
- Mode choice: Did the skill choose the right mode or wrapper?
- Restraint: Did it stay concise for narrow questions?
- Source quality: Were sources credible and relevant?
- Recency: Did it prefer current data and flag stale numbers?
- Contradictions: Did it surface conflicting estimates instead of hiding them?
- Decision value: Did the answer make the next product or business action clearer?
- Output shape: Did the answer match the expected structure for the request?

## Verdicts
- `pass`: no meaningful business risk
- `soft_fail`: useful, but a repeatable instruction gap may exist
- `hard_fail`: likely to cause the wrong decision or mislead the user

## Reopen threshold
Reopen `SKILL.md` when:
- one `hard_fail` occurs, or
- two `soft_fail` entries share the same root cause
