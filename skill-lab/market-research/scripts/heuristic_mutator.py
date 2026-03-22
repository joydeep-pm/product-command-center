from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_context(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def insert_after_heading(text: str, heading: str, block: str) -> str | None:
    if block.strip() in text:
        return None
    needle = f"{heading}\n"
    if needle not in text:
        return None
    return text.replace(needle, f"{needle}{block}\n", 1)


def apply_glp1_evidence_rule(text: str, _: dict) -> tuple[str | None, str]:
    block = (
        "- For manufacturing landscapes, separate `verified molecule-specific manufacturers` from "
        "`capability anchors`. Do not imply that a peptide-capable CDMO is a confirmed API supplier "
        "for a named GLP-1 molecule unless direct evidence says so.\n"
        "- If the user asks for a full manufacturer map, add an explicit row for `molecule-specific "
        "manufacturer attribution` and mark it `Unavailable` where public evidence stops."
    )
    updated = insert_after_heading(text, "### Handling Uncertainty", block)
    return updated, "added molecule-specific manufacturer attribution guidance"


def apply_table_gap_rule(text: str, _: dict) -> tuple[str | None, str]:
    if "Not publicly disclosed" in text:
        return None, "benchmark gap guidance already present"
    pattern = re.compile(
        r"### Evidence-Backed Comparison Matrix\n\| Company \| Requested benchmark dimension\(s\) \| "
        r"Verified metric / signal \| Source \| Date \| Gaps \|\n"
        r"\|---------\|----------------------------------\|--------------------------\|--------\|------\|------\|\n"
        r"\| \.\.\.     \| \.\.\.                              \| \.\.\. / Not publicly disclosed \| \.\.\. \| \.\.\. \| \.\.\. \|"
    )
    if pattern.search(text):
        return None, "comparison matrix already contains disclosure gap guidance"
    return None, "comparison matrix template not found"


def apply_recency_expansion(text: str, context: dict) -> tuple[str | None, str]:
    top_rerun_issues = context.get("validation_summary", {}).get("top_rerun_issue_patterns", [])
    if not any("pricing" in issue.lower() or "machine-readable" in issue.lower() for issue, _ in top_rerun_issues):
        return None, "no recency/disclosure issue in rerun summary"
    block = (
        "- If a current source exists only as a visual chart or partial disclosure, say that the metric is "
        "`not machine-readable from the official source` rather than inventing precision."
    )
    updated = insert_after_heading(text, "### Handling Uncertainty", block)
    return updated, "added machine-readable disclosure guidance"


STRATEGIES = (
    apply_glp1_evidence_rule,
    apply_recency_expansion,
    apply_table_gap_rule,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Conservative mutator for SKILL.md autoresearch loops.")
    parser.add_argument("--target", required=True, help="Path to the mutable artifact.")
    parser.add_argument("--context", required=True, help="Path to the iteration context JSON.")
    parser.add_argument("--state", required=True, help="Path to persistent mutator state JSON.")
    args = parser.parse_args()

    target_path = Path(args.target)
    context_path = Path(args.context)
    state_path = Path(args.state)

    text = target_path.read_text(encoding="utf-8")
    context = load_context(context_path)
    state = load_context(state_path)
    attempted = set(state.get("attempted_strategies", []))

    for strategy in STRATEGIES:
        if strategy.__name__ in attempted:
            continue
        updated, note = strategy(text, context)
        attempted.add(strategy.__name__)
        state["attempted_strategies"] = sorted(attempted)
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        if updated is not None and updated != text:
            target_path.write_text(updated, encoding="utf-8")
            print(
                json.dumps(
                    {
                        "changed": True,
                        "strategy": strategy.__name__,
                        "note": note,
                    }
                )
            )
            return
        print(
            json.dumps(
                {
                    "changed": False,
                    "strategy": strategy.__name__,
                    "note": note,
                }
            )
        )
        return

    print(json.dumps({"changed": False, "strategy": None, "note": "no remaining heuristic strategies"}))


if __name__ == "__main__":
    main()
