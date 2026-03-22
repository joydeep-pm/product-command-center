# Real-Request Validation Workflow

The market research skill is now frozen at the instruction level. Do not edit `/Users/joy/autoresearch/skill-lab/market-research/source/SKILL.md` again unless real usage exposes a concrete failure.

## Goal
Use real market-research requests to decide whether the frozen skill still holds up outside the synthetic evaluator.

## Files
- Request log: `/Users/joy/autoresearch/skill-lab/market-research/validation/real_requests.jsonl`
- Request template: `/Users/joy/autoresearch/skill-lab/market-research/validation/real_requests_template.jsonl`
- Review rubric: `/Users/joy/autoresearch/skill-lab/market-research/validation/review_rubric.md`
- Summary script: `/Users/joy/autoresearch/skill-lab/market-research/scripts/summarize_validation.py`

## Logging a request
Append one JSON object per line to `validation/real_requests.jsonl`.

Required fields:
- `id`: stable request id
- `submitted_at`: ISO timestamp
- `prompt`: the real user request
- `run_status`: `pending` or `reviewed`

Recommended fields:
- `requester`: who asked
- `context`: product/company context that mattered
- `expected_shape`: `quick_answer`, `single_mode_report`, `multi_mode_wrapper`, or another short label
- `review`: object containing `verdict`, `issues`, `strengths`, and `recommended_skill_patch`

## Review standard
After the skill is used on a real request, review the output against `review_rubric.md`.
Only reopen `SKILL.md` if at least one issue is both:
- repeatable across multiple requests, or
- severe enough to cause the wrong business decision from one request

## Summarize the log
```bash
cd /Users/joy/autoresearch/skill-lab/market-research
python3 scripts/summarize_validation.py
```

## Reopen rule
Reopen the skill only when the validation summary shows a concrete defect pattern, such as:
- repeated wrong mode choice
- repeated over-answering on quick questions
- stale source handling on current-data prompts
- failure to surface contradictory estimates
- weak recommendation framing in go/no-go prompts
