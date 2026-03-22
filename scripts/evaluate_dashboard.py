from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "app" / "dashboard.html"
DATA_PATH = ROOT / "data" / "command_center_data.json"
DOC_PATH = ROOT / "docs" / "source_brief.md"
METRIC_SPEC_PATH = ROOT / "docs" / "dashboard_metric_spec.md"

REQUIRED_SECTIONS = {
    "executive_snapshot": ["executive summary", "at a glance", "snapshot"],
    "strategic_imperatives": ["strategic imperatives", "strategic", "imperative"],
    "quarterly_roadmap": ["q1", "q2", "q3", "q4", "roadmap"],
    "epic_register": ["epic", "initiative"],
    "loss_intelligence": ["loss", "demo loss", "loss intelligence"],
    "competitive_parity": ["parity", "competitor", "competitive"],
    "compliance_firewall": ["dpdpa", "compliance", "ecl", "eir", "audit"],
    "market_expansion": ["gcc", "islamic", "capital markets", "mca", "scf"],
    "resource_plan": ["pd", "capacity", "resource", "headcount"],
    "risks_dependencies": ["risk", "dependency", "constraint"],
    "source_index": ["source", "document", "report", "deck"],
}

DECISION_SUPPORT_TERMS = [
    "loss",
    "priority",
    "risk",
    "dependency",
    "rationale",
    "quarter",
    "business value",
    "sales angle",
    "market",
    "compliance",
]


def pct(n: int, d: int) -> float:
    return round((n / d) * 100, 1) if d else 0.0


def score_ratio(hits: int, total: int, max_points: float) -> float:
    return round((hits / total) * max_points, 1) if total else 0.0


def find_function_body(script: str, fn_name: str) -> str:
    match = re.search(rf"function\s+{re.escape(fn_name)}\s*\([^)]*\)\s*\{{(.*?)\n\}}", script, re.DOTALL)
    return match.group(1).lower() if match else ""


def main() -> None:
    html_raw = HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    html = html_raw.lower()
    data = json.loads(DATA_PATH.read_text()) if DATA_PATH.exists() else {}
    brief = DOC_PATH.read_text(encoding="utf-8", errors="ignore").lower() if DOC_PATH.exists() else ""
    metric_spec = METRIC_SPEC_PATH.read_text(encoding="utf-8", errors="ignore").lower() if METRIC_SPEC_PATH.exists() else ""

    section_hits = {}
    for name, needles in REQUIRED_SECTIONS.items():
        section_hits[name] = any(needle in html for needle in needles)

    coverage_count = sum(1 for ok in section_hits.values() if ok)
    coverage_pct = pct(coverage_count, len(REQUIRED_SECTIONS))
    coverage_score = score_ratio(coverage_count, len(REQUIRED_SECTIONS), 15)

    decision_terms_found = sum(1 for term in DECISION_SUPPORT_TERMS if term in html)
    epic_ids_found = len(set(re.findall(r"\b[A-Z]{2,}(?:-[0-9]{2}[a-z]?|-[0-9]{1,3}[a-z]?|-[0-9]{1,3})\b", html_raw)))
    decision_support_score = min(
        15.0,
        round(score_ratio(decision_terms_found, len(DECISION_SUPPORT_TERMS), 10) + min(epic_ids_found, 20) * 0.25, 1),
    )

    script = html_raw
    render_overview = find_function_body(script, "renderOverview")
    render_risks = find_function_body(script, "renderRisks")
    render_source_index = find_function_body(script, "renderSourceIndex")
    render_strategy = find_function_body(script, "renderStrategy")
    get_epics = find_function_body(script, "getEpics")

    binding_checks = {
        "loads_command_center_json": "command_center_data.json" in script and "fetch(" in script,
        "uses_source_data_state": "SOURCE_DATA" in script,
        "source_index_bound": "meta.sources" in script and "pdf_notes" in script,
        "dependency_bound": "topic_map" in script,
        "resource_bound": "resource_plan" in script,
        "loss_intelligence_bound": "loss_intelligence" in script,
        "quarter_summary_bound": "quarter_summary" in script,
        "roadmap_epics_bound": "getworkbookepics" in get_epics and "roadmap_master" in script,
        "parity_bound": "competitive_parity" in script and "getparitydata" in render_strategy,
        "strategic_summary_bound": "strategic_summary" in script and "source_data" in render_strategy,
        "overview_uses_source_data": "source_data" in render_overview,
        "strategy_uses_source_data": "getparitydata" in render_strategy or "source_data" in render_strategy,
        "risks_uses_source_data": "source_data" in render_risks,
        "trace_tags_present": "trace-tag" in script,
    }
    dynamic_binding_score = score_ratio(sum(binding_checks.values()), len(binding_checks), 25)

    traceability_checks = {
        "has_source_brief": bool(brief),
        "has_metric_spec": bool(metric_spec),
        "has_source_data": bool(data),
        "shows_source_index_ui": "source index" in html,
        "shows_source_files": sum(1 for token in ["strategy deck", "strategy report", "roadmap pdf", "roadmap master workbook"] if token in html) >= 3,
        "render_source_index_bound": "sourcemeta" in render_source_index or "meta.sources" in render_source_index,
    }
    traceability_score = score_ratio(sum(traceability_checks.values()), len(traceability_checks), 10)

    render_checks = {
        "has_html": bool(re.search(r"<html", html)),
        "has_style": "<style" in html,
        "has_viewport": "viewport" in html,
        "has_media_queries": "@media" in html,
        "has_script": "<script" in html,
        "has_data_artifacts": DATA_PATH.exists() and DOC_PATH.exists(),
    }
    render_integrity_score = score_ratio(sum(render_checks.values()), len(render_checks), 10)

    status_query_body = find_function_body(script, "renderStatusQueryMatrix")
    gallery_rollup_body = find_function_body(script, "getGalleryStatusRows")
    quarter_rollup_body = find_function_body(script, "getQuarterStatusRows")
    operating_metrics_checks = {
        "has_status_query_matrix_ui": "status query matrix" in html,
        "has_vertical_rollup": "statusbyvertical" in html and "by vertical" in html,
        "has_horizontal_rollup": "statusbyhorizontal" in html and "by horizontal" in html,
        "has_quarter_rollup": "statusbyquarter" in html and "by quarter" in html,
        "renders_status_query_matrix": "renderstatusquerymatrix" in render_overview and "statusbyvertical" in status_query_body,
        "uses_gallery_status_rollups": "st.galstatus" in gallery_rollup_body and "getepicst" in gallery_rollup_body,
        "uses_quarter_status_rollups": "deriveaggregatestatus" in quarter_rollup_body and "q_meta" in quarter_rollup_body,
        "has_revenue_unlock_metric": "revenue unlock" in html,
        "has_delivery_confidence_metric": "delivery confidence" in html,
        "metric_spec_defines_operating_metrics": "revenue unlock by quarter" in metric_spec and "delivery confidence by quarter" in metric_spec,
    }
    operating_metrics_score = score_ratio(sum(operating_metrics_checks.values()), len(operating_metrics_checks), 25)

    penalties: list[dict[str, object]] = []
    if "loss_intelligence" not in script and "top 5 addressable fy26 losses" in html:
        penalties.append(
            {
                "label": "hardcoded_loss_intelligence",
                "points": 8,
                "reason": "Top-loss intelligence is still rendered from hardcoded HTML instead of workbook-derived data.",
            }
        )
    if "executivebaseline" not in render_overview and "quartersummary" not in render_overview and "fy27 roadmap" in html:
        penalties.append(
            {
                "label": "hardcoded_exec_metrics",
                "points": 5,
                "reason": "Executive metrics in the overview are still hardcoded and not bound to extracted source summaries.",
            }
        )
    if "COMPLIANCE_PANEL_DEFAULT" in script and "source_data" not in find_function_body(script, "getCompliancePanelEntries"):
        penalties.append(
            {
                "label": "static_compliance_panel",
                "points": 4,
                "reason": "Compliance command panel is still driven by local defaults rather than extracted source tables.",
            }
        )
    if "strategic_summary" not in script or "source_data" not in render_strategy:
        penalties.append(
            {
                "label": "static_strategy_narrative",
                "points": 2,
                "reason": "Strategic pillars are still static narrative blocks rather than a source-bound synthesis.",
            }
        )
    if "const PARITY_DATA" in script and "competitive_parity" not in script:
        penalties.append(
            {
                "label": "static_parity_surface",
                "points": 4,
                "reason": "Competitive parity view is still detached from workbook parity data.",
            }
        )
    if "status query matrix" not in html:
        penalties.append(
            {
                "label": "missing_status_queryability",
                "points": 6,
                "reason": "Leadership still cannot slice status by vertical, horizontal, and quarter from the overview.",
            }
        )
    if "revenue unlock" not in html:
        penalties.append(
            {
                "label": "missing_revenue_unlock_metric",
                "points": 4,
                "reason": "The command center does not yet show quarter-level revenue unlock tied to roadmap delivery.",
            }
        )
    if "delivery confidence" not in html:
        penalties.append(
            {
                "label": "missing_delivery_confidence_metric",
                "points": 4,
                "reason": "The dashboard lacks a forward-looking confidence metric for quarter plans.",
            }
        )

    penalty_points = sum(int(item["points"]) for item in penalties)
    total_score = round(
        max(
            0.0,
            coverage_score
            + decision_support_score
            + dynamic_binding_score
            + traceability_score
            + render_integrity_score
            + operating_metrics_score
            - penalty_points,
        ),
        1,
    )

    report = {
        "html": str(HTML_PATH),
        "score": total_score,
        "coverage_pct": coverage_pct,
        "scores": {
            "coverage": coverage_score,
            "decision_support": decision_support_score,
            "dynamic_binding": dynamic_binding_score,
            "traceability": traceability_score,
            "render_integrity": render_integrity_score,
            "operating_metrics": operating_metrics_score,
        },
        "section_hits": section_hits,
        "binding_checks": binding_checks,
        "traceability_checks": traceability_checks,
        "render_checks": render_checks,
        "operating_metrics_checks": operating_metrics_checks,
        "penalties": penalties,
        "hard_checks": {
            **render_checks,
            "requires_browser_verification": True,
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
