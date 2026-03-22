from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = ROOT / "source" / "SKILL.md"
DEFAULT_EVAL = "python3 scripts/evaluate_skill.py"
DEFAULT_VALIDATION = "python3 scripts/summarize_validation.py"
DEFAULT_RESULTS = ROOT / "results.tsv"
DEFAULT_RUNS = ROOT / "runs" / "autoresearch_loop"
DEFAULT_MUTATOR = "python3 scripts/heuristic_mutator.py --target \"$AUTORESEARCH_TARGET\" --context \"$AUTORESEARCH_CONTEXT\" --state \"$AUTORESEARCH_MUTATOR_STATE\""


@dataclass
class IterationResult:
    changed: bool
    kept: bool
    score_before: float
    score_after: float
    strategy: str | None
    note: str
    eval_report_path: Path
    context_path: Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def run_command(command: str, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        shell=True,
        text=True,
        capture_output=True,
        env=env,
    )


def run_json_command(command: str, cwd: Path, env: dict[str, str] | None = None) -> dict:
    result = run_command(command, cwd, env)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command did not return JSON: {command}\nstdout:\n{result.stdout}") from exc


def append_result(results_path: Path, score: float, status: str, description: str) -> None:
    line = f"{now_iso()}\tuncommitted\t{score:.1f}\t{status}\t{description}\n"
    with results_path.open("a", encoding="utf-8") as handle:
        handle.write(line)


def read_recent_results(results_path: Path, limit: int = 5) -> list[str]:
    if not results_path.exists():
        return []
    lines = results_path.read_text(encoding="utf-8").splitlines()
    return lines[-limit:]


def build_context(
    target_path: Path,
    results_path: Path,
    baseline_eval: dict,
    validation_summary: dict,
    iteration: int,
) -> dict:
    return {
        "target_path": str(target_path),
        "iteration": iteration,
        "baseline_score": baseline_eval.get("score"),
        "baseline_penalties": baseline_eval.get("penalties", []),
        "validation_summary": validation_summary,
        "recent_results": read_recent_results(results_path),
    }


def run_mutator(
    command: str,
    cwd: Path,
    target_path: Path,
    context_path: Path,
    mutator_state_path: Path,
    iteration_dir: Path,
) -> dict:
    env = os.environ.copy()
    env["AUTORESEARCH_ROOT"] = str(ROOT)
    env["AUTORESEARCH_TARGET"] = str(target_path)
    env["AUTORESEARCH_CONTEXT"] = str(context_path)
    env["AUTORESEARCH_MUTATOR_STATE"] = str(mutator_state_path)
    env["AUTORESEARCH_ITERATION_DIR"] = str(iteration_dir)
    result = run_command(command, cwd, env)
    mutator_log = iteration_dir / "mutator_stdout.txt"
    mutator_err = iteration_dir / "mutator_stderr.txt"
    mutator_log.write_text(result.stdout, encoding="utf-8")
    mutator_err.write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(
            f"mutator failed with exit code {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    if not result.stdout.strip():
        return {"changed": False, "strategy": None, "note": "mutator returned no output"}
    try:
        return json.loads(result.stdout.strip().splitlines()[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"mutator output was not JSON:\n{result.stdout}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a conservative autoresearch loop for SKILL.md.")
    parser.add_argument("--iterations", type=int, default=10, help="Maximum iterations to attempt.")
    parser.add_argument(
        "--stop-after-no-improvement",
        type=int,
        default=3,
        help="Stop after this many consecutive reverted/no-change iterations.",
    )
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Path to the mutable artifact.")
    parser.add_argument("--evaluate-command", default=DEFAULT_EVAL, help="JSON-producing evaluation command.")
    parser.add_argument(
        "--validation-command",
        default=DEFAULT_VALIDATION,
        help="JSON-producing validation summary command used for context only.",
    )
    parser.add_argument(
        "--mutator-command",
        default=DEFAULT_MUTATOR,
        help="Shell command that mutates the target in place. Context is passed via AUTORESEARCH_* env vars.",
    )
    parser.add_argument("--results", default=str(DEFAULT_RESULTS), help="Path to results.tsv.")
    parser.add_argument("--run-dir", default=str(DEFAULT_RUNS), help="Directory where loop artifacts are stored.")
    parser.add_argument(
        "--keep-on-equal",
        action="store_true",
        help="Keep a candidate if the evaluator score is unchanged. Off by default to prevent drift.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute baseline and write context, but do not run the mutator.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cwd = ROOT
    target_path = Path(args.target).resolve()
    results_path = Path(args.results).resolve()
    runs_root = Path(args.run_dir).resolve()
    run_id = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    run_root = runs_root / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    mutator_state_path = run_root / "mutator_state.json"
    mutator_state_path.write_text(json.dumps({"attempted_strategies": []}, indent=2), encoding="utf-8")

    baseline_eval = run_json_command(args.evaluate_command, cwd)
    validation_summary = run_json_command(args.validation_command, cwd)
    best_score = float(baseline_eval["score"])

    baseline_path = run_root / "baseline_eval.json"
    baseline_path.write_text(json.dumps(baseline_eval, indent=2), encoding="utf-8")
    (run_root / "baseline_validation.json").write_text(json.dumps(validation_summary, indent=2), encoding="utf-8")

    append_result(
        results_path,
        best_score,
        "baseline",
        f"autoresearch runner baseline from {target_path.name} (run {run_id})",
    )

    if args.dry_run:
        print(
            json.dumps(
                {
                    "run_id": run_id,
                    "mode": "dry_run",
                    "baseline_score": best_score,
                    "run_root": str(run_root),
                },
                indent=2,
            )
        )
        return

    consecutive_non_improvements = 0
    kept_iterations = 0
    history: list[dict] = []

    for iteration in range(1, args.iterations + 1):
        iteration_dir = run_root / f"iteration_{iteration:03d}"
        iteration_dir.mkdir(parents=True, exist_ok=True)
        before_text = target_path.read_text(encoding="utf-8")

        context = build_context(target_path, results_path, baseline_eval, validation_summary, iteration)
        context_path = iteration_dir / "context.json"
        context_path.write_text(json.dumps(context, indent=2), encoding="utf-8")
        (iteration_dir / "before.md").write_text(before_text, encoding="utf-8")

        mutator_result = run_mutator(
            args.mutator_command,
            cwd,
            target_path,
            context_path,
            mutator_state_path,
            iteration_dir,
        )

        after_text = target_path.read_text(encoding="utf-8")
        changed = after_text != before_text and bool(mutator_result.get("changed"))
        (iteration_dir / "after.md").write_text(after_text, encoding="utf-8")

        if not changed:
            target_path.write_text(before_text, encoding="utf-8")
            consecutive_non_improvements += 1
            append_result(
                results_path,
                best_score,
                "skip",
                f"autoresearch iteration {iteration}: {mutator_result.get('note', 'no change')}",
            )
            history.append(
                {
                    "iteration": iteration,
                    "changed": False,
                    "kept": False,
                    "score_before": best_score,
                    "score_after": best_score,
                    "strategy": mutator_result.get("strategy"),
                    "note": mutator_result.get("note", "no change"),
                }
            )
            if consecutive_non_improvements >= args.stop_after_no_improvement:
                break
            continue

        eval_report = run_json_command(args.evaluate_command, cwd)
        eval_report_path = iteration_dir / "eval_report.json"
        eval_report_path.write_text(json.dumps(eval_report, indent=2), encoding="utf-8")
        score_after = float(eval_report["score"])
        keep = score_after > best_score or (args.keep_on_equal and score_after == best_score)

        if keep:
            best_score = score_after
            baseline_eval = eval_report
            kept_iterations += 1
            consecutive_non_improvements = 0
            append_result(
                results_path,
                score_after,
                "keep",
                f"autoresearch iteration {iteration}: {mutator_result.get('note', 'kept candidate')}",
            )
        else:
            target_path.write_text(before_text, encoding="utf-8")
            consecutive_non_improvements += 1
            append_result(
                results_path,
                score_after,
                "revert",
                f"autoresearch iteration {iteration}: reverted after {mutator_result.get('note', 'no improvement')}",
            )

        history.append(
            {
                "iteration": iteration,
                "changed": True,
                "kept": keep,
                "score_before": history[-1]["score_after"] if history else float((run_json_command(args.evaluate_command, cwd))["score"]) if False else float(json.loads(baseline_path.read_text(encoding="utf-8"))["score"]),
                "score_after": score_after,
                "strategy": mutator_result.get("strategy"),
                "note": mutator_result.get("note", ""),
            }
        )

        if consecutive_non_improvements >= args.stop_after_no_improvement:
            break

    summary = {
        "run_id": run_id,
        "run_root": str(run_root),
        "iterations_requested": args.iterations,
        "iterations_completed": len(history),
        "kept_iterations": kept_iterations,
        "best_score": best_score,
        "stopped_for_no_improvement": consecutive_non_improvements >= args.stop_after_no_improvement,
        "history": history,
        "target_path": str(target_path),
        "mutator_command": args.mutator_command,
    }
    summary_path = run_root / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
