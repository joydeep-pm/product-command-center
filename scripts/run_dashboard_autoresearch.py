from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = ROOT / "app" / "dashboard.html"
DEFAULT_EVAL = "python3 scripts/evaluate_dashboard.py"
DEFAULT_RESULTS = ROOT / "results.tsv"
DEFAULT_RUNS = ROOT / "runs" / "html_autoresearch"
DEFAULT_MUTATOR = "python3 scripts/html_heuristic_mutator.py --target \"$AUTORESEARCH_TARGET\" --context \"$AUTORESEARCH_CONTEXT\" --state \"$AUTORESEARCH_MUTATOR_STATE\""


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
    with results_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{now_iso()}\tuncommitted\t{score:.1f}\t{status}\t{description}\n")


def read_recent_results(results_path: Path, limit: int = 5) -> list[str]:
    if not results_path.exists():
        return []
    return results_path.read_text(encoding="utf-8").splitlines()[-limit:]


def build_context(target_path: Path, results_path: Path, baseline_eval: dict, iteration: int) -> dict:
    return {
        "target_path": str(target_path),
        "iteration": iteration,
        "baseline_score": baseline_eval.get("score"),
        "baseline_penalties": baseline_eval.get("penalties", []),
        "operating_metrics_checks": baseline_eval.get("operating_metrics_checks", {}),
        "recent_results": read_recent_results(results_path),
    }


def run_mutator(command: str, cwd: Path, target_path: Path, context_path: Path, state_path: Path, iteration_dir: Path) -> dict:
    env = os.environ.copy()
    env["AUTORESEARCH_ROOT"] = str(ROOT)
    env["AUTORESEARCH_TARGET"] = str(target_path)
    env["AUTORESEARCH_CONTEXT"] = str(context_path)
    env["AUTORESEARCH_MUTATOR_STATE"] = str(state_path)
    env["AUTORESEARCH_ITERATION_DIR"] = str(iteration_dir)
    result = run_command(command, cwd, env)
    (iteration_dir / "mutator_stdout.txt").write_text(result.stdout, encoding="utf-8")
    (iteration_dir / "mutator_stderr.txt").write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(
            f"mutator failed with exit code {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    if not result.stdout.strip():
        return {"changed": False, "strategy": None, "note": "mutator returned no output"}
    return json.loads(result.stdout.strip().splitlines()[-1])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a conservative autoresearch loop for app/dashboard.html.")
    parser.add_argument("--iterations", type=int, default=6, help="Maximum iterations to attempt.")
    parser.add_argument(
        "--stop-after-no-improvement",
        type=int,
        default=2,
        help="Stop after this many consecutive reverted/no-change iterations.",
    )
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Path to the mutable artifact.")
    parser.add_argument("--evaluate-command", default=DEFAULT_EVAL, help="JSON-producing evaluation command.")
    parser.add_argument("--mutator-command", default=DEFAULT_MUTATOR, help="Shell command for the dashboard mutator.")
    parser.add_argument("--results", default=str(DEFAULT_RESULTS), help="Path to results.tsv.")
    parser.add_argument("--run-dir", default=str(DEFAULT_RUNS), help="Directory for loop artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Only compute the baseline and write run scaffolding.")
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
    state_path = run_root / "mutator_state.json"
    state_path.write_text(json.dumps({"attempted_strategies": []}, indent=2), encoding="utf-8")

    baseline_eval = run_json_command(args.evaluate_command, cwd)
    best_score = float(baseline_eval["score"])
    (run_root / "baseline_eval.json").write_text(json.dumps(baseline_eval, indent=2), encoding="utf-8")
    append_result(results_path, best_score, "baseline", f"html autoresearch baseline from {target_path.name} (run {run_id})")

    if args.dry_run:
        print(json.dumps({"run_id": run_id, "mode": "dry_run", "baseline_score": best_score, "run_root": str(run_root)}, indent=2))
        return

    consecutive_non_improvements = 0
    kept_iterations = 0
    history: list[dict] = []

    for iteration in range(1, args.iterations + 1):
        iteration_dir = run_root / f"iteration_{iteration:03d}"
        iteration_dir.mkdir(parents=True, exist_ok=True)
        before_text = target_path.read_text(encoding="utf-8")
        context = build_context(target_path, results_path, baseline_eval, iteration)
        context_path = iteration_dir / "context.json"
        context_path.write_text(json.dumps(context, indent=2), encoding="utf-8")
        (iteration_dir / "before.html").write_text(before_text, encoding="utf-8")

        mutator_result = run_mutator(args.mutator_command, cwd, target_path, context_path, state_path, iteration_dir)
        after_text = target_path.read_text(encoding="utf-8")
        changed = after_text != before_text and bool(mutator_result.get("changed"))
        (iteration_dir / "after.html").write_text(after_text, encoding="utf-8")

        if not changed:
            target_path.write_text(before_text, encoding="utf-8")
            consecutive_non_improvements += 1
            append_result(results_path, best_score, "skip", f"html autoresearch iteration {iteration}: {mutator_result.get('note', 'no change')}")
            history.append({"iteration": iteration, "changed": False, "kept": False, "score_before": best_score, "score_after": best_score, "strategy": mutator_result.get("strategy"), "note": mutator_result.get("note", "no change")})
            if consecutive_non_improvements >= args.stop_after_no_improvement:
                break
            continue

        eval_report = run_json_command(args.evaluate_command, cwd)
        (iteration_dir / "eval_report.json").write_text(json.dumps(eval_report, indent=2), encoding="utf-8")
        score_after = float(eval_report["score"])
        keep = score_after > best_score

        if keep:
            best_score = score_after
            baseline_eval = eval_report
            kept_iterations += 1
            consecutive_non_improvements = 0
            append_result(results_path, best_score, "keep", f"html autoresearch iteration {iteration}: {mutator_result.get('note', 'kept improvement')}")
        else:
            target_path.write_text(before_text, encoding="utf-8")
            consecutive_non_improvements += 1
            append_result(results_path, score_after, "revert", f"html autoresearch iteration {iteration}: {mutator_result.get('note', 'reverted')} (score {best_score:.1f}->{score_after:.1f})")

        history.append({"iteration": iteration, "changed": True, "kept": keep, "score_before": context["baseline_score"], "score_after": score_after, "strategy": mutator_result.get("strategy"), "note": mutator_result.get("note", "")})
        if consecutive_non_improvements >= args.stop_after_no_improvement:
            break

    summary = {
        "run_id": run_id,
        "run_root": str(run_root),
        "target_path": str(target_path),
        "baseline_score": float((run_root / "baseline_eval.json").read_text() and json.loads((run_root / "baseline_eval.json").read_text())["score"]),
        "final_score": best_score,
        "kept_iterations": kept_iterations,
        "history": history,
    }
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
