from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "source" / "SKILL.md"
CASES_PATH = ROOT / "tests" / "cases.json"

MODE_HEADINGS = {
    "Mode 1": "### Mode 1: Market Sizing (TAM / SAM / SOM)",
    "Mode 2": "### Mode 2: Competitive Landscape",
    "Mode 3": "### Mode 3: Customer & Segment Analysis",
    "Mode 4": "### Mode 4: Pricing Research",
    "Mode 5": "### Mode 5: Opportunity Assessment",
    "quick question": "### For Quick Questions",
    "complex research": "### For Complex Research",
}

TOKEN_PATTERNS = {
    "TAM": [r"\btam\b"],
    "SAM": [r"\bsam\b"],
    "SOM": [r"\bsom\b"],
    "confidence": [r"\bconfidence\b"],
    "so what": [r"so what"],
    "competitive set": [r"competitive set"],
    "positioning": [r"positioning map", r"\bpositioning\b"],
    "gaps": [r"\bgaps\b", r"underserved"],
    "moat": [r"\bmoat\b", r"moats"],
    "segment": [r"\bsegment\b", r"segments"],
    "priority": [r"\bpriority\b", r"prioritize"],
    "pain point": [r"pain point", r"pain points"],
    "channels": [r"\bchannels\b"],
    "pricing": [r"\bpricing\b"],
    "value metric": [r"value metric", r"value metrics"],
    "tiers": [r"\btiers\b", r"tiered"],
    "architecture": [r"pricing architecture", r"\barchitecture\b"],
    "GO": [r"go / conditional go / no-go", r"\bgo\b", r"recommendation"],
    "risks": [r"\brisks\b", r"\brisk\b"],
    "fit": [r"\bfit\b"],
    "timing": [r"\btiming\b"],
    "next steps": [r"next steps"],
    "sources": [r"\bsources\b", r"source\(s\)"],
    "benchmark": [r"\bbenchmark\b", r"\bbenchmarking\b", r"comparison matrix"],
    "coverage": [r"coverage checklist", r"requested slice", r"full market map", r"covered / partial / unavailable"],
    "primary metric": [r"primary metric", r"primary requested metric", r"requested metric"],
    "insufficient evidence": [r"insufficient evidence", r"cannot be defended", r"not defensible"],
    "proxy": [r"\bproxy\b", r"proxy metrics"],
    "source ledger": [r"source ledger", r"source trail", r"source table"],
    "assumptions": [r"\bassumptions\b", r"assumption ledger"],
    "sensitivity": [r"\bsensitivity\b", r"scenario range", r"base / upside / downside", r"range analysis"],
    "universe": [r"candidate universe", r"market map universe", r"\buniverse\b"],
    "shortlist": [r"deep-dive shortlist", r"deep dive shortlist", r"\bshortlist\b"],
    "module coverage": [r"module coverage", r"capability coverage", r"product modules", r"capability grid"],
    "breadth": [r"search beyond", r"beyond the user-named", r"broader universe", r"do not stop at the companies named"],
}


def score_ratio(hits: int, total: int, max_points: float) -> float:
    return round((hits / total) * max_points, 1) if total else 0.0


def section_map(markdown: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_title: str | None = None
    current_lines: list[str] = []
    in_code_block = False

    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        if not in_code_block and re.match(r"^###\s+.+$", line):
            if current_title is not None:
                sections[current_title] = "\n".join(current_lines).strip()
            current_title = line.strip()
            current_lines = []
            continue
        if current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections[current_title] = "\n".join(current_lines).strip()

    return sections


def has_any_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def token_hit(text: str, token: str) -> bool:
    patterns = TOKEN_PATTERNS.get(token, [re.escape(token)])
    return has_any_pattern(text, patterns)


def has_output_contract(section_text: str) -> bool:
    return "**output format**" in section_text.lower() and "```" in section_text


def has_mode5_decision_rule(mode5_text: str) -> bool:
    return has_any_pattern(
        mode5_text.lower(),
        [r"evaluating whether to enter a market", r"launch a product", r"go/no-go"],
    )


def has_conflict_guidance(skill_text: str) -> bool:
    return has_any_pattern(
        skill_text.lower(),
        [
            r"if .*sources .*disagree",
            r"conflicting source",
            r"conflicting estimates",
            r"contradict",
            r"show both",
            r"surface.*conflict",
        ],
    )


def has_recency_guidance(skill_text: str) -> bool:
    return has_any_pattern(
        skill_text.lower(),
        [
            r"always prefer recent data",
            r"latest numbers",
            r"check recency",
            r"older than 12 months",
            r"note the date of data",
        ],
    )


def has_quantified_benchmark_guidance(mode2_text: str) -> bool:
    return has_any_pattern(
        mode2_text.lower(),
        [
            r"benchmark",
            r"comparison matrix",
            r"structured table",
            r"not publicly disclosed",
        ],
    )


def has_coverage_completeness_guidance(skill_text: str, mode2_text: str) -> bool:
    combined = f"{skill_text}\n{mode2_text}".lower()
    return has_any_pattern(
        combined,
        [
            r"full market map",
            r"multiple layers",
            r"multiple geograph",
            r"enumerate each requested slice",
            r"covered, partially covered, or unavailable",
            r"coverage checklist",
        ],
    )


def has_primary_metric_guidance(mode1_text: str, uncertainty_text: str) -> bool:
    combined = f"{mode1_text}\n{uncertainty_text}".lower()
    return has_any_pattern(combined, [r"primary metric", r"requested metric"]) and has_any_pattern(
        combined,
        [
            r"insufficient evidence for a defensible estimate",
            r"cannot be defended",
            r"best available proxy",
            r"proxy metrics",
            r"do not swap",
        ],
    )


def has_market_sizing_depth_guidance(mode1_text: str, uncertainty_text: str) -> bool:
    combined = f"{mode1_text}\n{uncertainty_text}".lower()
    return (
        has_any_pattern(combined, TOKEN_PATTERNS["source ledger"])
        and has_any_pattern(combined, TOKEN_PATTERNS["assumptions"])
        and has_any_pattern(combined, TOKEN_PATTERNS["sensitivity"])
    )


def has_landscape_depth_guidance(mode2_text: str) -> bool:
    text = mode2_text.lower()
    return (
        has_any_pattern(text, TOKEN_PATTERNS["universe"])
        and has_any_pattern(text, TOKEN_PATTERNS["shortlist"])
        and has_any_pattern(text, TOKEN_PATTERNS["module coverage"])
    )


def has_competitor_breadth_guidance(mode2_text: str) -> bool:
    return has_any_pattern(mode2_text.lower(), TOKEN_PATTERNS["breadth"])


def main() -> None:
    skill = SKILL_PATH.read_text(encoding="utf-8")
    skill_l = skill.lower()
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    sections = section_map(skill)
    quick_text = sections.get(MODE_HEADINGS["quick question"], "")
    complex_text = sections.get(MODE_HEADINGS["complex research"], "")
    mode1_text = sections.get(MODE_HEADINGS["Mode 1"], "")
    mode2_text = sections.get(MODE_HEADINGS["Mode 2"], "")
    mode5_text = sections.get(MODE_HEADINGS["Mode 5"], "")
    uncertainty_text = skill.split("### Handling Uncertainty", 1)[1] if "### Handling Uncertainty" in skill else ""
    conflict_guidance = has_conflict_guidance(skill)
    recency_guidance = has_recency_guidance(skill)
    benchmark_guidance = has_quantified_benchmark_guidance(mode2_text)
    coverage_guidance = has_coverage_completeness_guidance(skill, mode2_text)
    primary_metric_guidance = has_primary_metric_guidance(mode1_text, uncertainty_text)
    market_sizing_depth_guidance = has_market_sizing_depth_guidance(mode1_text, uncertainty_text)
    landscape_depth_guidance = has_landscape_depth_guidance(mode2_text)
    competitor_breadth_guidance = has_competitor_breadth_guidance(mode2_text)

    structure_checks = {
        "has_frontmatter_name": re.search(r"^---.*?name:\s*market-research", skill, re.DOTALL | re.MULTILINE) is not None,
        "has_description": "description:" in skill,
        "has_overview": "## overview" in skill_l,
        "has_core_principles": "## core principles" in skill_l,
        "has_research_modes": "## research modes" in skill_l,
        "has_execution_guidelines": "## research execution guidelines" in skill_l,
        "has_adapting_to_context": "## adapting to context" in skill_l,
        "has_output_delivery": "## output delivery" in skill_l,
    }
    structure_score = score_ratio(sum(structure_checks.values()), len(structure_checks), 15)

    mode_checks = {
        "mode_1": MODE_HEADINGS["Mode 1"] in sections,
        "mode_2": MODE_HEADINGS["Mode 2"] in sections,
        "mode_3": MODE_HEADINGS["Mode 3"] in sections,
        "mode_4": MODE_HEADINGS["Mode 4"] in sections,
        "mode_5": MODE_HEADINGS["Mode 5"] in sections,
        "quick_questions": MODE_HEADINGS["quick question"] in sections,
        "complex_research": MODE_HEADINGS["complex research"] in sections,
    }
    mode_score = score_ratio(sum(mode_checks.values()), len(mode_checks), 15)

    quality_checks = {
        "confidence_levels": "confidence" in skill_l,
        "uncertainty_section": "## handling uncertainty" in skill_l,
        "quality_checklist": "- [ ]" in skill,
        "web_powered": "web-powered" in skill_l or "web-powered market research" in skill_l,
        "primary_sources": "prioritize primary sources" in skill_l,
        "triangulate": "triangulate" in skill_l,
        "recent_data": "older than 12 months" in skill_l or "recency matters" in skill_l,
        "distinguishes_estimates": "estimate vs. a verified figure" in skill_l or "verified facts, reasonable estimates, and speculation" in skill_l,
        "conflicting_sources_guidance": conflict_guidance,
        "benchmark_table_guidance": benchmark_guidance,
        "coverage_completeness_guidance": coverage_guidance,
        "primary_metric_guidance": primary_metric_guidance,
        "market_sizing_depth_guidance": market_sizing_depth_guidance,
        "landscape_depth_guidance": landscape_depth_guidance,
        "competitor_breadth_guidance": competitor_breadth_guidance,
    }
    quality_score = score_ratio(sum(quality_checks.values()), len(quality_checks), 15)

    output_checks = {
        "mode_1_output_contract": has_output_contract(sections.get(MODE_HEADINGS["Mode 1"], "")),
        "mode_2_output_contract": has_output_contract(sections.get(MODE_HEADINGS["Mode 2"], "")),
        "mode_3_output_contract": has_output_contract(sections.get(MODE_HEADINGS["Mode 3"], "")),
        "mode_4_output_contract": has_output_contract(sections.get(MODE_HEADINGS["Mode 4"], "")),
        "mode_5_output_contract": has_output_contract(sections.get(MODE_HEADINGS["Mode 5"], "")),
        "quick_question_restraint": has_any_pattern(
            quick_text,
            [r"answer directly", r"directly with sources"],
        )
        and has_any_pattern(
            quick_text,
            [r"don't produce a full report", r"do not produce a full report"],
        ),
        "complex_research_wrapper": has_any_pattern(
            complex_text,
            [r"single comprehensive document", r"flows logically"],
        )
        and has_any_pattern(
            complex_text,
            [r"opportunity assessment", r"wrapper"],
        ),
    }
    output_score = score_ratio(sum(output_checks.values()), len(output_checks), 15)

    references = re.findall(r"`([^`]+\.md)`", skill)
    reference_results = []
    for ref in references:
        ref_path = (SKILL_PATH.parent / ref).resolve()
        reference_results.append({"ref": ref, "exists": ref_path.exists()})
    reference_checks = {
        "all_references_resolve": all(item["exists"] for item in reference_results),
        "has_research_prompts_ref": any("research-prompts.md" in item["ref"] for item in reference_results),
        "has_data_sources_ref": any("data-sources.md" in item["ref"] for item in reference_results),
        "has_cases": len(cases) >= 10,
        "covers_all_modes": {mode for case in cases for mode in case["expected_modes"] if mode in MODE_HEADINGS} >= {"Mode 1", "Mode 2", "Mode 3", "Mode 4", "Mode 5", "quick question", "complex research"},
    }
    reference_score = score_ratio(sum(reference_checks.values()), len(reference_checks), 10)

    content_case_results = []
    content_hits = 0
    content_total = 0
    selection_case_results = []
    selection_hits = 0
    selection_total = 0

    for case in cases:
        case_type = case.get("case_type", "content")
        expected_modes = case["expected_modes"]

        if case_type == "content":
            expected_mode = expected_modes[0]
            section_title = MODE_HEADINGS.get(expected_mode)
            section_text = sections.get(section_title, "")
            section_text_l = section_text.lower()
            mode_exists = bool(section_text)
            token_results = {token: token_hit(section_text_l, token) for token in case["must_include"]}
            extra_checks: dict[str, bool] = {}

            if expected_mode == "quick question":
                extra_checks["answers_directly"] = output_checks["quick_question_restraint"]
            elif expected_mode == "Mode 4":
                extra_checks["has_explicit_output_contract"] = has_output_contract(section_text)
            elif expected_mode == "Mode 5":
                extra_checks["uses_go_no_go_recommendation"] = token_hit(section_text_l, "GO")
                extra_checks["has_next_steps"] = token_hit(section_text_l, "next steps")

            case_hits = int(mode_exists) + sum(token_results.values()) + sum(extra_checks.values())
            case_total = 1 + len(token_results) + len(extra_checks)
            content_hits += case_hits
            content_total += case_total
            content_case_results.append(
                {
                    "id": case["id"],
                    "prompt": case["prompt"],
                    "expected_mode": expected_mode,
                    "section_title": section_title,
                    "mode_exists": mode_exists,
                    "token_results": token_results,
                    "extra_checks": extra_checks,
                    "score": round((case_hits / case_total) * 100, 1),
                }
            )
            continue

        mode_results = {
            mode: (MODE_HEADINGS.get(mode) in sections if mode in MODE_HEADINGS else False)
            for mode in expected_modes
        }
        selection_checks = {
            "mode_identification_rule": "identify which mode(s) apply" in skill_l,
        }
        if case.get("requires_direct_answer"):
            selection_checks["direct_answer_rule"] = output_checks["quick_question_restraint"]
        if case.get("forbid_full_report"):
            selection_checks["quick_question_overrides_default_report"] = output_checks["quick_question_restraint"] and "### default: markdown document" in skill_l
        if case.get("requires_wrapper"):
            selection_checks["single_wrapper_rule"] = output_checks["complex_research_wrapper"]
        if case.get("primary_mode") == "Mode 5":
            selection_checks["mode_5_primary_for_decision"] = has_mode5_decision_rule(mode5_text) and output_checks["complex_research_wrapper"]
        if case.get("requires_conflict_surfacing"):
            selection_checks["surfaces_conflicting_sources"] = conflict_guidance
        if case.get("requires_recency"):
            selection_checks["recency_rule"] = recency_guidance
        if case.get("requires_date_flag"):
            selection_checks["flags_old_or_dated_data"] = has_any_pattern(
                skill_l,
                [r"older than 12 months", r"note the date of data", r"check recency"],
            )
        if case.get("requires_quantified_benchmark_table"):
            selection_checks["quantified_benchmark_rule"] = benchmark_guidance
        if case.get("requires_coverage_checklist"):
            selection_checks["coverage_completeness_rule"] = coverage_guidance
        if case.get("requires_primary_metric_discipline"):
            selection_checks["primary_metric_discipline_rule"] = primary_metric_guidance
        if case.get("requires_source_ledger"):
            selection_checks["market_sizing_source_ledger_rule"] = has_any_pattern(
                f"{mode1_text}\n{uncertainty_text}".lower(),
                TOKEN_PATTERNS["source ledger"],
            )
        if case.get("requires_assumptions_ledger"):
            selection_checks["market_sizing_assumptions_rule"] = has_any_pattern(
                f"{mode1_text}\n{uncertainty_text}".lower(),
                TOKEN_PATTERNS["assumptions"],
            )
        if case.get("requires_sensitivity_analysis"):
            selection_checks["market_sizing_sensitivity_rule"] = has_any_pattern(
                f"{mode1_text}\n{uncertainty_text}".lower(),
                TOKEN_PATTERNS["sensitivity"],
            )
        if case.get("requires_universe_table"):
            selection_checks["landscape_universe_rule"] = has_any_pattern(
                mode2_text.lower(),
                TOKEN_PATTERNS["universe"],
            )
        if case.get("requires_deep_dive_shortlist"):
            selection_checks["landscape_shortlist_rule"] = has_any_pattern(
                mode2_text.lower(),
                TOKEN_PATTERNS["shortlist"],
            )
        if case.get("requires_module_coverage_grid"):
            selection_checks["landscape_module_coverage_rule"] = has_any_pattern(
                mode2_text.lower(),
                TOKEN_PATTERNS["module coverage"],
            )
        if case.get("requires_search_beyond_named_examples"):
            selection_checks["competitor_breadth_rule"] = competitor_breadth_guidance

        case_hits = sum(mode_results.values()) + sum(selection_checks.values())
        case_total = len(mode_results) + len(selection_checks)
        selection_hits += case_hits
        selection_total += case_total
        selection_case_results.append(
            {
                "id": case["id"],
                "prompt": case["prompt"],
                "expected_modes": expected_modes,
                "mode_results": mode_results,
                "selection_checks": selection_checks,
                "score": round((case_hits / case_total) * 100, 1),
            }
        )

    behavioral_score = score_ratio(content_hits, content_total, 20)
    selection_score = score_ratio(selection_hits, selection_total, 10)

    penalties = []
    if not reference_checks["all_references_resolve"]:
        penalties.append(
            {
                "label": "broken_local_references",
                "points": 10,
                "reason": "SKILL.md references local markdown files that do not resolve from the skill directory.",
            }
        )
    if not output_checks["mode_4_output_contract"]:
        penalties.append(
            {
                "label": "missing_pricing_output_contract",
                "points": 8,
                "reason": "Mode 4 explains workflow but does not define a concrete output format, so pricing prompts are under-specified.",
            }
        )
    if not conflict_guidance:
        penalties.append(
            {
                "label": "missing_conflict_resolution_guidance",
                "points": 6,
                "reason": "The skill says to triangulate sources but does not tell the agent how to report conflicting estimates when credible sources disagree.",
            }
        )
    if not benchmark_guidance:
        penalties.append(
            {
                "label": "missing_quantified_benchmark_guidance",
                "points": 6,
                "reason": "Benchmark-driven landscape requests need an evidence-backed comparison matrix, but the skill does not require one.",
            }
        )
    if not coverage_guidance:
        penalties.append(
            {
                "label": "missing_coverage_completeness_guidance",
                "points": 6,
                "reason": "Exhaustive market-map requests can silently omit layers or geographies because the skill does not require a coverage checklist.",
            }
        )
    if not primary_metric_guidance:
        penalties.append(
            {
                "label": "missing_primary_metric_discipline",
                "points": 8,
                "reason": "When a named primary metric cannot be defended, the skill must force an explicit insufficiency call and separate proxy metrics.",
            }
        )
    if not market_sizing_depth_guidance:
        penalties.append(
            {
                "label": "missing_market_sizing_depth_guidance",
                "points": 8,
                "reason": "Investor-grade sizing requests need a source ledger, assumptions ledger, and sensitivity/range handling instead of a single summarized number.",
            }
        )
    if not landscape_depth_guidance:
        penalties.append(
            {
                "label": "missing_landscape_depth_guidance",
                "points": 8,
                "reason": "Exhaustive landscape requests need a candidate universe, deep-dive shortlist, and module/capability coverage grid.",
            }
        )
    if not competitor_breadth_guidance:
        penalties.append(
            {
                "label": "missing_competitor_breadth_guidance",
                "points": 6,
                "reason": "The skill must tell the agent to search beyond the few firms named in the prompt, or market maps stay too shallow.",
            }
        )

    total_score = round(
        max(
            0.0,
            structure_score
            + mode_score
            + quality_score
            + output_score
            + reference_score
            + behavioral_score
            + selection_score
            - sum(item["points"] for item in penalties),
        ),
        1,
    )

    report = {
        "skill": str(SKILL_PATH),
        "score": total_score,
        "scores": {
            "structure": structure_score,
            "modes": mode_score,
            "quality": quality_score,
            "output_contracts": output_score,
            "references_and_eval": reference_score,
            "behavioral_cases": behavioral_score,
            "selection_and_restraint": selection_score,
        },
        "structure_checks": structure_checks,
        "mode_checks": mode_checks,
        "quality_checks": quality_checks,
        "output_checks": output_checks,
        "reference_checks": reference_checks,
        "reference_results": reference_results,
        "behavioral_case_results": content_case_results,
        "selection_case_results": selection_case_results,
        "penalties": penalties,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
