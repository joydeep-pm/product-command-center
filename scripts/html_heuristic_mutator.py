from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def insert_after(text: str, needle: str, block: str) -> str | None:
    if block.strip() in text:
        return None
    if needle not in text:
        return None
    return text.replace(needle, needle + block, 1)


def insert_before(text: str, needle: str, block: str) -> str | None:
    if block.strip() in text:
        return None
    if needle not in text:
        return None
    return text.replace(needle, block + needle, 1)


def replace_once(text: str, old: str, new: str) -> str | None:
    if old not in text:
        return None
    return text.replace(old, new, 1)


REVENUE_CSS = """
.signal-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-bottom:18px}
@media(max-width:1100px){.signal-grid{grid-template-columns:1fr}}
.signal-list{display:flex;flex-direction:column;gap:10px}
.signal-row{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;padding:10px 0;border-bottom:1px solid var(--border)}
.signal-row:last-child{border-bottom:none}
.signal-name{font-size:11.5px;font-weight:600;color:var(--text)}
.signal-copy{font-size:10px;color:var(--muted);margin-top:2px;line-height:1.45}
.signal-side{display:flex;flex-direction:column;align-items:flex-end;gap:5px;min-width:120px}
.signal-val{font-family:Georgia,serif;font-size:20px;line-height:1}
.signal-meta{font-size:10px;color:var(--muted);text-align:right}
.signal-bar{width:110px;height:6px;background:var(--border);border-radius:99px;overflow:hidden}
.signal-bar-fill{height:100%;border-radius:99px}
"""

REVENUE_HTML = """
      <div class="signal-grid" id="opsSignalGrid">
        <div class="card">
          <div class="card-title" style="margin-bottom:4px">Revenue Unlock by Quarter</div>
          <div class="card-sub" style="margin-bottom:12px">Workbook-traceable lost pipeline that becomes addressable if the target quarter ships on time.</div>
          <div class="signal-list" id="revenueUnlock"></div>
        </div>
        <div class="card" id="deliveryConfidenceShell" style="display:none"></div>
      </div>
"""

REVENUE_JS = """
function getRevenueUnlockRows() {
  const rows = getLossIntelligenceRows();
  return ['Q1','Q2','Q3','Q4'].map(q => {
    const quarterRows = rows.filter(row => String(row['Quarter Fix'] || '').trim() === q);
    const total = quarterRows.reduce((sum, row) => sum + (Number(row['Loss (₹ Cr)']) || 0), 0);
    const critical = quarterRows.filter(row => /critical/i.test(String(row['Recovery Priority'] || ''))).length;
    const tier = total >= 15 ? 'Critical' : total >= 5 ? 'Watch' : 'Low';
    return {q, total, count: quarterRows.length, critical, tier};
  });
}
function renderRevenueUnlock() {
  const host = document.getElementById('revenueUnlock');
  if(!host) return;
  const rows = getRevenueUnlockRows();
  host.innerHTML = rows.map(row => {
    const tone = row.tier === 'Critical' ? 'var(--red)' : row.tier === 'Watch' ? 'var(--amber)' : 'var(--green)';
    return `<div class="signal-row">
      <div>
        <div class="signal-name">${row.q} unlock</div>
        <div class="signal-copy">${row.count} mapped losses · ${row.critical} critical recoveries tied to this quarter</div>
      </div>
      <div class="signal-side">
        <div class="signal-val" style="color:${tone}">₹${row.total.toFixed(1)} Cr</div>
        <div class="signal-meta">${row.tier}</div>
      </div>
    </div>`;
  }).join('');
}
"""

DELIVERY_HTML = """
        <div class="card" id="deliveryConfidenceCard">
          <div class="card-title" style="margin-bottom:4px">Delivery Confidence</div>
          <div class="card-sub" style="margin-bottom:12px">Forward-looking quarter confidence after blocked work, at-risk work, and dependency concentration are applied.</div>
          <div class="signal-list" id="deliveryConfidence"></div>
        </div>
"""

DELIVERY_JS = """
function quarterDependencyPressure(q) {
  const quarterEpicIds = getEpics().filter(epic => epic.q === q).map(epic => epic.id);
  const topicRows = SOURCE_DATA?.workbook?.topic_map || [];
  let linked = 0;
  topicRows.forEach(row => {
    const text = `${row['EPIC'] || ''} ${row['Connected To'] || ''} ${row['Successor'] || ''}`;
    if(quarterEpicIds.some(id => text.includes(id))) linked += 1;
  });
  return linked >= 3;
}
function getDeliveryConfidenceRows() {
  const epics = getEpics();
  return ['Q1','Q2','Q3','Q4'].map(q => {
    const quarterEpics = epics.filter(epic => epic.q === q);
    const counts = summarizeStatuses(quarterEpics.map(epic => getEpicSt(epic.id)));
    const pressure = quarterDependencyPressure(q);
    const blocked = counts['Blocked'] || 0;
    const risk = counts['At Risk'] || 0;
    const score = Math.max(0, 100 - (blocked * 20) - (risk * 10) - (pressure ? 10 : 0));
    const band = score >= 75 ? 'High' : score >= 50 ? 'Medium' : 'Low';
    return {
      q,
      score,
      band,
      pressure,
      blocked,
      risk,
    };
  });
}
function renderDeliveryConfidence() {
  const host = document.getElementById('deliveryConfidence');
  if(!host) return;
  const rows = getDeliveryConfidenceRows();
  host.innerHTML = rows.map(row => {
    const tone = row.score >= 75 ? 'var(--green)' : row.score >= 50 ? 'var(--amber)' : 'var(--red)';
    return `<div class="signal-row">
      <div>
        <div class="signal-name">${row.q} confidence</div>
        <div class="signal-copy">${row.blocked} blocked · ${row.risk} at risk${row.pressure ? ' · dependency concentration detected' : ''}</div>
      </div>
      <div class="signal-side">
        <div class="signal-val" style="color:${tone}">${row.score}</div>
        <div class="signal-bar"><div class="signal-bar-fill" style="width:${row.score}%;background:${tone}"></div></div>
        <div class="signal-meta">${row.band}</div>
      </div>
    </div>`;
  }).join('');
}
"""


def apply_revenue_unlock_metric(text: str, _: dict) -> tuple[str | None, str]:
    if 'id="revenueUnlock"' in text:
        return None, "revenue unlock metric already present"

    updated = text
    if REVENUE_CSS.strip() not in updated:
        updated = insert_after(
            updated,
            ".status-chip.ns{background:rgba(80,96,128,0.15);color:var(--muted);border-color:rgba(80,96,128,0.2)}\n",
            REVENUE_CSS,
        ) or updated

    status_anchor = """          </div>
        </div>
      </div>
      <div class="divider"></div>
"""
    updated = insert_after(updated, status_anchor, REVENUE_HTML)
    if updated is None:
        return None, "could not place revenue unlock card"

    updated = insert_before(updated, "function getDependencyWatchEntries() {\n", REVENUE_JS)
    if updated is None:
        return None, "could not place revenue unlock helper"

    updated = replace_once(
        updated,
        "  renderStatusQueryMatrix();\n}",
        "  renderStatusQueryMatrix();\n  renderRevenueUnlock();\n}",
    )
    if updated is None:
        return None, "could not wire revenue unlock renderer"

    return updated, "added revenue unlock by quarter metric"


def apply_delivery_confidence_metric(text: str, _: dict) -> tuple[str | None, str]:
    if 'id="deliveryConfidence"' in text:
        return None, "delivery confidence metric already present"
    if 'id="deliveryConfidenceShell"' not in text:
        return None, "delivery confidence shell not present"

    updated = replace_once(text, '<div class="card" id="deliveryConfidenceShell" style="display:none"></div>', DELIVERY_HTML)
    if updated is None:
        return None, "could not place delivery confidence card"

    updated = insert_before(updated, "function getDependencyWatchEntries() {\n", DELIVERY_JS)
    if updated is None:
        return None, "could not place delivery confidence helper"

    updated = replace_once(
        updated,
        "  renderStatusQueryMatrix();\n  renderRevenueUnlock();\n}",
        "  renderStatusQueryMatrix();\n  renderRevenueUnlock();\n  renderDeliveryConfidence();\n}",
    )
    if updated is None:
        return None, "could not wire delivery confidence renderer"

    return updated, "added delivery confidence by quarter metric"


STRATEGIES = (
    apply_revenue_unlock_metric,
    apply_delivery_confidence_metric,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Conservative mutator for dashboard autoresearch.")
    parser.add_argument("--target", required=True, help="Path to app/dashboard.html")
    parser.add_argument("--context", required=True, help="Path to iteration context JSON")
    parser.add_argument("--state", required=True, help="Path to persistent mutator state JSON")
    args = parser.parse_args()

    target_path = Path(args.target)
    state_path = Path(args.state)
    text = target_path.read_text(encoding="utf-8")
    context = load_json(Path(args.context))
    state = load_json(state_path)
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
            print(json.dumps({"changed": True, "strategy": strategy.__name__, "note": note}))
            return
        print(json.dumps({"changed": False, "strategy": strategy.__name__, "note": note}))
        return

    print(json.dumps({"changed": False, "strategy": None, "note": "no remaining heuristic strategies"}))


if __name__ == "__main__":
    main()
