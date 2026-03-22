# Todo

- [x] Review current workspace and identify the source artifacts for the command center.
- [x] Define the command-center scope beyond visual design.
- [x] Scaffold the autoresearch workflow files: `program.md`, `results.tsv`, evaluator, and extraction scripts.
- [x] Extract the provided PDFs/XLSX into structured repo artifacts.
- [x] Run the initial evaluator and capture a baseline for the current dashboard.
- [x] Start the first targeted improvement cycle on `app/dashboard.html`.
- [x] Replace hardcoded roadmap and AOP EPIC structures with workbook-backed data.
- [x] Bind the remaining strategy narrative surfaces to extracted source data.

# Review

- The command center scope is based on the provided strategy deck, strategy report, roadmap PDF, and roadmap workbook.
- The workbook provides the strongest structured source of truth and is used as the primary data spine.
- The PDF documents are summarized into a source brief so dashboard iterations can preserve executive framing, ROI language, and strategic narrative.
- The current HTML was rendered through a local server and loaded correctly in the browser. The only console issue observed was a missing `favicon.ico`.
- The current baseline rubric score is intentionally heuristic. Browser verification remains required before treating any score increase as real progress.
- First improvement cycle completed: added source traceability in the overview and compliance/capacity panels in the risks view.
- Next execution step is to continue reducing hardcoded business data inside the HTML and progressively bind more sections to `command_center_data.json`.
- Second improvement cycle completed: evaluator is now strict, overview metrics are source-bound, and source discrepancies are surfaced instead of hidden.
- Third improvement cycle completed: roadmap, AOP, epic modal context, and competitive parity are now sourced from workbook data instead of static dashboard arrays.
- Browser verification confirmed workbook-backed quarter totals, non-numeric PD states (`Ongoing`, `TBD`), and epic modal rationale render correctly with zero console errors.
- The stricter evaluator now scores the dashboard at `98.0` and explicitly withholds full score until the strategic narrative blocks are source-bound rather than static prose.
- Fourth improvement cycle completed: strategic imperatives, moats, friction zones, and the key insight panel now render from `strategic_summary` inside `command_center_data.json` instead of hardcoded prose in the HTML.
- Extraction now emits a reusable `strategic_summary` artifact, so the strategy narrative lives with the source-derived data instead of the view layer.
- Browser verification confirmed the strategy tab renders source-tagged narrative cards with zero console errors.
- The evaluator now checks for `strategic_summary` binding and returns `100.0` only after the strategy narrative is source-backed.
- Next execution step is to reduce the remaining curated fallback arrays and start scoring against factual consistency checks, not just structural source binding.
## Skill Autoresearch

- [x] Import the market research skill into the repo as a mutable artifact.
- [x] Define a skill-specific autoresearch program, evaluator, and test prompts.
- [x] Document the workflow for iterating on the skill safely.
- [x] Extend the evaluator from structural checks to case-based behavioral checks.
- [x] Patch the skill only where the stricter evaluator exposes a concrete gap.
- [x] Re-run the stricter evaluator and log the iteration outcome.
- [x] Add negative and ambiguous prompt cases for mode restraint and wrapper selection.
- [x] Extend the evaluator to score primary-mode choice and quick-question overreach.
- [x] Patch the skill only if the new cases expose a concrete guidance gap.
- [x] Re-run the evaluator and log this iteration.
- [x] Add contradiction-handling and latest-data prompt cases.
- [x] Extend the evaluator to score source-conflict surfacing and recency-sensitive prompts.
- [x] Patch the skill only if these new cases expose a concrete instruction gap.
- [x] Re-run the evaluator and log the iteration.
- [x] Freeze `source/SKILL.md` and add a real-request validation workflow around it.
- [x] Add validation artifacts for logging, reviewing, and summarizing real market-research requests.
- [x] Dry-run the validation tooling and record the result.
- [x] Reopen the skill based on real-request validation failures.
- [x] Encode the real-request failure modes in the evaluator and case suite.
- [x] Patch the skill with stricter benchmarking, coverage-completeness, and primary-metric insufficiency rules.
- [x] Re-run the evaluator and log the reopened iteration.
- [x] Create a second real-validation batch that preserves the original reviewed outputs.
- [x] Re-run the 5 real prompts against the hardened skill with current sources and stricter evidence tables.
- [x] Review the rerun batch against the first batch's fail reasons and record which failures disappeared.
- [x] Add a real unattended autoresearch runner on top of the market-research evaluator and logs.
- [x] Add a conservative mutator path so the runner can operate without git or manual intervention.
- [x] Document how to run the loop safely and how to plug in a stronger mutator later.
- [x] Smoke-test the autonomous runner and record the outcome.

## HTML Autoresearch Revival

- [x] Define a metric spec for the command-center operating metrics, including status by vertical, horizontal, and quarter.
- [x] Implement the new status-queryability surfaces in `app/dashboard.html` using live dashboard state.
- [x] Tighten `scripts/evaluate_dashboard.py` so the HTML loop has headroom below `100.0` until those capabilities exist.
- [x] Build or adapt an unattended HTML autoresearch runner with bounded iterations and safe keep/revert logic.
- [x] Run the HTML autoresearch loop, verify the kept result in browser/evaluator terms, and record the outcome.

## Status Console Upgrade

- [x] Add overview controls to filter status by slice, quarter, status, and search text.
- [x] Add a compact executive summary for the currently filtered status view.
- [x] Add JSON and CSV export for the filtered status view.
- [x] Verify the status console and exports in browser without console regressions.

## Skill Runner Execution

- [x] Add the market-research runner execution steps and inspect the current runner, mutator, and evaluator state.
- [x] Dry-run the market-research autoresearch runner to confirm baseline and artifact paths.
- [x] Run a bounded autonomous loop on the market-research skill and capture the run artifacts.
- [x] Verify whether the loop improved the evaluator or correctly exited with no-op behavior.

## Review Addendum

- New task: apply autoresearch to the market research skill from `product-skills-main.zip`.
- Imported the market research skill into `/Users/joy/autoresearch/skill-lab/market-research` as a separate mutable artifact.
- Added a skill-specific program, evaluator, test cases, and workflow docs for the market research skill.
- Baseline skill score was `85.0`; the first defect was broken local reference paths in `SKILL.md`.
- First skill iteration fixed those helper-doc references and raised the evaluator score to `100.0`.
- Next execution step for the skill lab is to move beyond structural checks and add behavioral evals that test mode selection, output quality, and restraint on real prompts.
- Second skill iteration completed: the evaluator now parses mode sections safely, checks real prompt cases, and penalizes missing output contracts instead of just missing headings.
- The stricter behavioral evaluator initially dropped the score to `89.0`, exposing a real gap in `Mode 4: Pricing Research` rather than a cosmetic wording issue.
- Patched `Mode 4` with a concrete pricing output template covering competitor pricing, value metrics, tiers, pricing architecture, and the decision-level "So What".
- Re-ran the evaluator and recovered the score to `100.0`; all behavioral cases now pass with no penalties.
- Third skill iteration completed: the evaluator now includes negative and ambiguous prompt cases for quick-question restraint and multi-mode wrapper selection.
- Added selection-focused cases that verify `Mode 5` remains the primary wrapper for decision prompts and that quick questions stay direct instead of expanding into reports.
- Re-ran the stricter evaluator after expanding the case suite; the skill held at `100.0`, so no new `SKILL.md` patch was required in this iteration.
- Fourth skill iteration completed: added contradiction-handling and latest-data cases to the evaluator so the skill is tested against conflicting sources and explicitly current-data prompts.
- The recency checks already passed, but the contradiction case dropped the score to `91.9` because the skill did not explicitly tell the agent how to present conflicting estimates.
- Patched the uncertainty guidance to require showing both estimates with source names and dates, explaining the discrepancy, and avoiding false precision.
- Re-ran the evaluator and recovered the score to `100.0`; contradiction and recency cases now pass cleanly.
- Fifth phase started: the skill is now frozen and the lab has shifted from synthetic improvement to real-request validation.
- Added a validation workflow, review rubric, request log template, and summary script under `/Users/joy/autoresearch/skill-lab/market-research/validation`.
- Dry-ran the validation summary script against the empty real-request log; it returned `no_real_requests_logged`, which is the expected baseline state before production use.
- The next edits to `SKILL.md` should come only from repeatable failures in real-request reviews, not from more synthetic evaluator expansion.
- Logged the first real validation batch with 5 pending requests covering B2B LMS providers, GLP-1 manufacturers, data centers, open-weight LLMs, and the Indian loan-against-securities market.
- Ran the validation summary after logging the batch; the lab now reports `5` total requests, `5` pending, `0` reviewed, and no schema warnings.
- Refined the first real batch with explicit `primary_mode`, `expected_modes`, and `review_focus` fields so later reviews measure the frozen skill against the right target shape.
- Drafted five separate markdown outputs under `/Users/joy/autoresearch/skill-lab/market-research/outputs/real_batch_001` and linked each output path back into the live validation log.
- Verified that the validation log still parses cleanly after attaching output paths; all 5 requests remain `pending` review rather than `reviewed`.
- Performed a shell-based URL sanity check, but the environment returned generic `URLError` responses for all external links, so source-link verification remains inconclusive rather than failed.
- Reviewed the first real validation batch against the rubric and converted all 5 requests from `pending` to `reviewed`.
- Validation outcome: `3 soft_fail`, `2 hard_fail`; this is sufficient to reopen `SKILL.md` for instruction fixes.
- The dominant failure pattern is that broad benchmarking prompts are answered with useful synthesis but not enough quantified comparison structure, complete segmentation, or hard insufficiency handling when the primary requested metric cannot be defended.
- Reopen scope is now limited to the concrete root causes from that batch: benchmark requests need quantified comparison rules, exhaustive asks need explicit coverage-completeness rules, and market-sizing requests need a harder insufficiency posture when the named primary metric cannot be defended.
- Reopened the skill with new hard rules in `Mode 1`, `Mode 2`, `Quality Checks`, and `Handling Uncertainty` so exhaustive market maps cannot silently omit layers and benchmark-driven reports must carry evidence tables.
- Hardened the evaluator and case suite with real-batch-derived cases for quantified benchmarks, full coverage checklists, and primary-metric insufficiency handling; the reopened evaluator still passes at `100.0`.
- Created `real_batch_002` so the rerun can be compared side-by-side with the original reviewed outputs rather than overwriting them.
- Reran all 5 real prompts against the hardened skill and attached `rerun_output_path` plus `rerun_review` metadata to each validation record.
- Rerun outcome: `4 pass`, `1 soft_fail`.
- Failures that clearly disappeared: the open-weight LLM hard fail, the LAS hard fail, the data-center under-quantification soft fail, and the LMS module-comparison soft fail.
- Remaining weak surface: GLP-1 still lacks a fully evidenced molecule-by-molecule API-manufacturer map even after the harder coverage rules.
- HTML autoresearch revival completed: added a concrete operating-metric spec, live status queryability, `Revenue Unlock by Quarter`, and `Delivery Confidence` to the overview.
- Tightened the dashboard evaluator so the HTML loop dropped from `100.0` to `87.0` until the new operating metrics existed.
- Ran the unattended HTML loop under `/Users/joy/autoresearch/runs/html_autoresearch/20260321T223235+0530`; it kept two iterations and improved the evaluator from `87.0` to `100.0`.
- Browser QA caught a real loop defect the evaluator missed: the mutator inserted helper functions inside `getDependencyWatchEntries()`, which caused a runtime `ReferenceError`.
- Fixed both the live dashboard and the mutator, then re-verified the page at `http://127.0.0.1:8123/app/dashboard.html` with zero console errors and intact source-bound rendering.
- Final smoke test of the runner on the already-improved dashboard now exits safely with `0` kept iterations instead of corrupting the page.
- Status console upgrade completed: the overview now has a filterable status console with slice, quarter, status, and free-text search controls.
- Added a compact executive summary showing visible rows plus green/blue/amber/red counts for the currently filtered view.
- Added filtered JSON and CSV exports for the status console and verified both download paths by intercepting the generated blob downloads in browser.
- Browser verification confirmed `Vertical + Q1 + Gold` narrows the view to a single row, and the page remains at zero console errors after the new controls and exports.
- Smoke-tested the market-research autonomous runner in dry-run mode and confirmed it writes run artifacts under `/Users/joy/autoresearch/skill-lab/market-research/runs/autoresearch_loop`.
- Executed a bounded autonomous run at `/Users/joy/autoresearch/skill-lab/market-research/runs/autoresearch_loop/20260321T225154+0530`; the runner attempted two conservative mutations, reverted both because the evaluator stayed at `100.0`, then stopped for no improvement.
- Post-run verification confirmed the market-research skill still evaluates at `100.0` and the persisted `source/SKILL.md` matches the pre-run version rather than either reverted candidate.

## Skill Depth Hardening
- [x] Tighten evaluator around research depth, quantified market sizing, and competitor breadth
- [x] Add depth-oriented test cases for exhaustive market maps and defensible sizing
- [x] Patch market research skill instructions to force deeper evidence structures
- [x] Re-run evaluator and record the new baseline and post-fix score

## Review
- The earlier `100.0` was a false positive because the evaluator only checked for coverage and benchmark intent, not decision-grade depth.
- The depth hardening pass added new evaluator and case coverage for market-sizing source ledgers, assumptions/sensitivity, company-universe construction, shortlist logic, module/capability grids, and explicit search beyond user-named anchor firms.
- `SKILL.md` now forces investor-grade sizing outputs to include a source ledger plus assumptions/sensitivity and forces exhaustive landscapes to separate a broad universe from a deep-dive shortlist.
- Post-fix evaluation remains `100.0` and is saved in `/Users/joy/autoresearch/skill-lab/market-research/runs/iteration_006_depth_hardening.json`; this verifies the stricter evaluator and updated skill are aligned.
- Remaining risk: this is still an instruction/evaluator hardening pass. The next proof step is to rerun real prompts and confirm the outputs themselves are deeper, not just the skill file.

## Real Report Deepening
- [x] Inspect prior LMS, LAS, and GLP-1 reports plus validation metadata to identify exact depth gaps
- [x] Research current sources and draft deeper replacement reports for LMS, LAS, and GLP-1
- [x] Update validation artifacts, verify outputs, and summarize remaining gaps

- `real_batch_003` now exists with depth-focused rewrites for LMS, GLP-1, and LAS under `/Users/joy/autoresearch/skill-lab/market-research/outputs/real_batch_003`.
- The LMS rewrite is materially broader than prior batches: it adds a candidate universe, deep-dive shortlist, and denser module/capability grid rather than staying centered on the original named vendor set.
- The LAS rewrite now uses a real source ledger, explicit insufficiency posture, and a scenario range with sensitivity assumptions instead of stopping at a proxy bucket.
- The GLP-1 rewrite is better structured and broader, but still carries the same honest residual gap: molecule-specific API attribution remains materially weaker than formulation / launch evidence.
- Validation metadata now points to the new batch via `deepened_output_path` fields for `real_003`, `real_004`, and `real_007`; the summary script still returns `status: ok` with no schema warnings.

## Shared Command Center
- [x] Inspect current repo shape and choose the smallest migration path from static HTML to shared web app
- [x] Write the data model and API contract for live shared status
- [x] Scaffold the web app structure and persistence layer for internal shared use
- [x] Document deployment and operating assumptions for internal-only access
- Added a minimal shared-state server at `/Users/joy/autoresearch/webapp/server.js` that serves the dashboard, exposes a live state API, and writes an audit log without adding third-party runtime dependencies.
- Added file-backed shared persistence at `/Users/joy/autoresearch/data/live_dashboard_state.json` and `/Users/joy/autoresearch/data/dashboard_audit_log.jsonl` so the command center now has a single shared source of truth when served through the new server.
- Patched `/Users/joy/autoresearch/app/dashboard.html` to detect shared mode, pull server-backed status, keep theme/filter preferences local, and preserve local-mode fallback when the shared server is not present.
- Documented the architecture, API contract, and internal-only deployment assumptions in `/Users/joy/autoresearch/docs/shared_command_center_webapp.md`.
- Verified the server contract on port `8130`, including `GET /api/dashboard-state`, `POST /api/dashboard-state`, and `GET /api/audit-log`, then reset the state files so the scaffold is left clean rather than seeded with test data.

## Audit Panel
- [x] Inspect the overview layout and choose the insertion point for a live audit-log panel
- [x] Patch dashboard UI and client logic to fetch and render audit-log entries with local-mode fallback
- [x] Run the shared server, verify audit API and UI behavior, and update task tracking

## Review

- Added a `Recent Updates` card to the overview beside the source and dependency panels so stakeholders can see the latest shared-state changes without leaving the command center.
- Shared-mode clients now fetch `/api/audit-log` on load and after successful writes; local mode falls back to a single explanatory row instead of showing an empty broken panel.
- Audit notes are now specific for EPIC status changes, EPIC notes, gallery status, strategy pillar updates, hiring-track updates, decision updates, custom EPIC creation, and backup imports.
- Verified the shared server on `http://127.0.0.1:8130`: a `POST /api/dashboard-state` write produced an audit row that was immediately available via `GET /api/audit-log?limit=5`.
- Verified the served dashboard includes the audit panel markup and client hooks (`auditLogList`, `fetchAuditLog`, `renderAuditLog`).
- Browser automation remains blocked by the local Chrome session, so this verification is API- and served-HTML-based rather than a Playwright UI proof.

## Audit Metadata
- [x] Inspect current edit flows and design a minimal shared edit-metadata pattern
- [x] Patch dashboard UI and save paths to capture updated_by and reason for shared edits
- [x] Verify shared audit metadata round-trip and update task tracking

- Added lightweight top-bar audit controls so product editors can set `Updated by` and an optional one-shot `Reason for next live update` without interrupting the normal status-edit flow.
- Shared writes now send `actor`, `note`, and `reason` together; the backend persists `updated_reason` in the shared state envelope and `reason` in each audit entry.
- The audit panel now renders the reason explicitly when present, so stakeholders can distinguish a status change from the business justification behind it.
- Verified on `http://127.0.0.1:8130` with a live write using actor `Akhil PM` and reason `Customer compliance dependency is unresolved`; the POST response, `GET /api/dashboard-state`, and `GET /api/audit-log?limit=3` all returned the same metadata.
- Verified the served dashboard includes the new top-bar controls (`actorNameInput`, `reasonInput`) alongside the existing `Recent Updates` audit panel.

## Deploy Live
- [x] Inspect repo, git remote state, and deployment readiness
- [x] Determine the correct production architecture for shared live status on Vercel
- [x] Implement required persistence changes for live shared status
- [x] Push to GitHub and deploy to Vercel if credentials and environment allow

- Added Vercel-native API routes under `/Users/joy/autoresearch/api` and a shared storage layer under `/Users/joy/autoresearch/webapp/shared-store.js` so the deployed app no longer depends on the local JSON filesystem.
- Added `/Users/joy/autoresearch/package.json` with `@vercel/blob` and `/Users/joy/autoresearch/vercel.json` rewrites so `/dashboard` serves the existing HTML while `/api/*` stays dynamic.
- Linked the repo to the Vercel project `autoresearch`, created and linked a private Blob store `autoresearch-command-center`, and pulled the development env locally.
- Verified the Vercel-shaped runtime through `vercel dev` with `storage_mode: vercel-blob`, a successful state write, and a successful audit-log read.
- Reset the Blob-backed shared state and audit log back to a clean baseline after verification.
- Pushed the repo to `https://github.com/joydeep-pm/product-command-center` on branch `main` with initial commit `f72e86e`.
- Deployed both preview and stable production builds on Vercel; the stable alias is `https://autoresearch-fawn.vercel.app`.

## QA Sidebar Fix
- [x] Reproduce the reported sidebar failure against the live deployment in a browser
- [x] Identify the root cause in `app/dashboard.html`
- [x] Patch the runtime so inline dashboard actions bind reliably
- [x] Re-verify locally through `vercel dev` and on production after deploy

- The reported sidebar bug was real on production: clicking `Roadmap` left `pane-overview` active and the topbar title unchanged.
- Root cause was a dashboard-script parse failure caused by nested backticks inside inline-handler HTML template strings; this prevented the main script from initializing and left all inline UI actions dead.
- The final fix binds inline handlers at runtime and removes the parse-breaking handler strings, restoring sidebar navigation and adjacent controls such as the theme toggle.
- Verified on `https://autoresearch-fawn.vercel.app`: `Roadmap` activates `pane-roadmap`, the active nav state updates, the title updates to `Roadmap`, and the theme toggle flips to light mode with zero console errors.

## GitHub Push
- [ ] Inspect repo state and identify what should not be published
- [ ] Patch ignore rules or repo hygiene needed for a safe initial push
- [ ] Add GitHub remote, commit the publishable repo state, and push

## Production QA Sweep
- [x] Define the broader production QA scope and evidence targets
- [x] Exercise all major panes and shared status flows on production
- [x] Fix any defects found and verify them locally and on production
- [x] Record QA findings, verification evidence, and remaining concerns

- Broader production QA covered all six primary panes, status filtering, status exports, responsive rendering, editor enablement, live shared save, audit-log visibility, and the reversible shared-state update path on `https://autoresearch-fawn.vercel.app`.
- Verified navigation by clicking each sidebar item and confirming active pane, active nav state, and topbar title alignment with zero console errors.
- Verified the status console after async load: default view rendered `17` rows, scoped filtering (`Vertical` + `Q1` + `gold`) reduced correctly to a single row, and JSON/CSV exports generated download payloads with the expected MIME types and filenames.
- Verified responsive captures were generated for mobile, tablet, and desktop via the browse runner under `/Users/joy/autoresearch/.gstack/qa-reports/screenshots/prod-sweep-*.png` with no console errors on load.
- Verified shared edit mode on production using the configured editor key: the dashboard switched to `Shared Live`, `Editor Enabled`, and accepted a reversible EPIC status update for `COL-02a`.
- Verified the shared write path end to end: the temporary `COL-02a` status flip persisted, the audit log recorded the update, and the state was then restored to the true empty baseline via the live API so production state is clean again.
- No new product defect was found in this pass. The remaining concern is operational rather than functional: read access is still public to anyone with the URL, while write access is protected only by the editor key.
- QA uncovered and fixed a real backend consistency bug in the live-state store: overwriting a single Vercel Blob pathname allowed stale reads after writes on production. The shared store now writes immutable versioned state/audit blobs and reads the latest object by prefix, which restored immediate read-after-write behavior on `GET /api/dashboard-state` and `GET /api/audit-log`.

## Access Control And Next Wave
- [x] Define the smallest real read-protection model for the live Vercel app and document the tradeoff versus full SSO
- [x] Implement viewer read protection across the dashboard and APIs, verify locally and on production, and document how stakeholders access the app
- [x] Apply the next autonomous command-center improvement on the protected app
- [x] Re-verify the improved app end to end and capture remaining concerns

- Added a real production viewer gate with `/access`, `VIEWER_KEY`, guarded dashboard/data routes, and protected APIs. The stable production URL now redirects anonymous users to the access page instead of serving the dashboard directly.
- Product editors still use `EDITOR_KEY` inside the dashboard; viewers and editors are now separated cleanly.
- Added `Lock View` to the top bar so a stakeholder can clear viewer access and return to the access screen without manually clearing cookies.
- Implemented `PD-to-Revenue Efficiency` in the overview from workbook-backed `quarter_summary` and `loss_intelligence`, using the metric spec thresholds (`High leverage`, `Moderate leverage`, `Low leverage`).
- Verified locally with `vercel dev`: anonymous `/` redirects to `/access`, protected APIs reject unauthorized reads, authenticated `/dashboard` loads, and the new efficiency card renders quarter values.
- Verified on production `https://autoresearch-fawn.vercel.app`: anonymous `/` redirects to `/access`, `GET /api/dashboard-state` returns `401` without viewer access, access-page login opens the dashboard, `PD-to-Revenue Efficiency` renders source-backed values after data load, and `Lock View` returns the user to `/access?next=%2Fdashboard`.
- Remaining concern: preview deployments are not yet consistently protected because Vercel preview env assignment for `VIEWER_KEY` is branch-scoped. Production is protected; preview protection should be completed in Vercel settings if preview URLs will be shared.
- Remaining concern: the GitHub repository itself is still outside the app-level viewer gate. The live app is protected, but repo visibility is a separate decision.
