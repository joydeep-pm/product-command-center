from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "validation" / "real_requests.jsonl"


def load_entries() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    entries: list[dict] = []
    for lineno, raw in enumerate(LOG_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        data = json.loads(line)
        data["_lineno"] = lineno
        entries.append(data)
    return entries


def main() -> None:
    entries = load_entries()
    reviewed = [entry for entry in entries if entry.get("run_status") == "reviewed"]
    pending = [entry for entry in entries if entry.get("run_status") != "reviewed"]
    rerun_reviewed = [entry for entry in entries if entry.get("rerun_status") == "reviewed"]

    verdicts = Counter()
    rerun_verdicts = Counter()
    issues = Counter()
    rerun_issues = Counter()
    patch_recommendations = 0
    schema_warnings: list[str] = []

    required_fields = {"id", "submitted_at", "prompt", "run_status"}
    for entry in entries:
        missing = sorted(required_fields - entry.keys())
        if missing:
            schema_warnings.append(f"line {entry['_lineno']}: missing fields {', '.join(missing)}")
        review = entry.get("review", {})
        verdict = review.get("verdict")
        if verdict:
            verdicts[verdict] += 1
        for issue in review.get("issues", []):
            issues[issue] += 1
        if review.get("recommended_skill_patch"):
            patch_recommendations += 1
        rerun_review = entry.get("rerun_review", {})
        rerun_verdict = rerun_review.get("verdict")
        if rerun_verdict:
            rerun_verdicts[rerun_verdict] += 1
        for issue in rerun_review.get("issues", []):
            rerun_issues[issue] += 1

    summary = {
        "log_path": str(LOG_PATH),
        "total_requests": len(entries),
        "reviewed_requests": len(reviewed),
        "pending_requests": len(pending),
        "verdict_counts": dict(verdicts),
        "rerun_reviewed_requests": len(rerun_reviewed),
        "rerun_verdict_counts": dict(rerun_verdicts),
        "top_issue_patterns": issues.most_common(5),
        "top_rerun_issue_patterns": rerun_issues.most_common(5),
        "recommended_skill_patch_count": patch_recommendations,
        "schema_warnings": schema_warnings,
        "status": "no_real_requests_logged" if len(entries) == 0 else "ok",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
