# FY27 Command-Center Operating Metrics

This dashboard is not a status board. It is a business command center for product, GTM, and leadership decisions.

The purpose of the metric layer is to answer five questions quickly:

1. What is the current delivery posture by product slice?
2. Which quarter unlocks or endangers revenue?
3. Which compliance gates are still blocking sellability?
4. How confident should leadership be in each quarter plan?
5. Is PD being spent on the right bets?

## Metric 1: Status Query Matrix

- Metric name: `Status by Vertical / Horizontal / Quarter`
- Business question: `Where are we green, amber, or red when leadership slices the portfolio differently?`
- Formula:
  - Vertical / horizontal status = explicit owner-set status if present, else aggregate of linked EPIC statuses.
  - Quarter status = aggregate of all EPIC statuses in the quarter.
  - Aggregate rule:
    - `Blocked` if any linked item is blocked
    - `At Risk` if none blocked but any linked item is at risk
    - `Completed` if all linked items are completed
    - `In Progress` if any linked item is in progress or completed
    - else `Not Started`
- Inputs:
  - `GALLERY`
  - `ST.galStatus`
  - `ST.epicStatus`
  - `workbook.roadmap_master`
- UI placement: `Overview`
- Thresholds:
  - `Green` = `Completed`
  - `Blue` = `In Progress`
  - `Amber` = `At Risk`
  - `Red` = `Blocked`

## Metric 2: Revenue Unlock by Quarter

- Metric name: `Revenue Unlock by Quarter`
- Business question: `How much lost or at-risk pipeline becomes addressable if the planned quarter ships on time?`
- Formula:
  - Sum `Loss (₹ Cr)` from `loss_intelligence` grouped by `Quarter Fix`
  - Use mapped EPICs and quarter fix from workbook source, not manual assumptions
- Inputs:
  - `workbook.loss_intelligence`
  - `workbook.roadmap_master`
- UI placement: `Overview`, near quarter execution metrics
- Thresholds:
  - `Critical` if quarter unlock is `>= ₹15 Cr`
  - `Watch` if quarter unlock is `₹5–15 Cr`
  - `Low` if quarter unlock is `< ₹5 Cr`

## Metric 3: Compliance Gate Clearance

- Metric name: `Compliance Gate Clearance`
- Business question: `Which regulated-deal blockers are still open, and what do they unlock when closed?`
- Formula:
  - Count open / in-progress / complete gates from compliance panel rows
  - Surface quarter ownership and linked EPICs
- Inputs:
  - `workbook.topic_map`
  - source-bound compliance command panel rows
  - linked EPIC statuses
- UI placement: `Risks`
- Thresholds:
  - `Red` if any Q1 or Q2 high-priority gate is blocked
  - `Amber` if gates are active but incomplete
  - `Green` if all currently due gates are completed

## Metric 4: Delivery Confidence by Quarter

- Metric name: `Quarter Delivery Confidence`
- Business question: `How much confidence should leadership place in each quarter plan, not just its task completion?`
- Formula:
  - Start at `100`
  - subtract `20` for each blocked EPIC in quarter
  - subtract `10` for each at-risk EPIC in quarter
  - subtract `10` if the quarter has heavy dependency concentration
  - floor at `0`
- Inputs:
  - `ST.epicStatus`
  - `workbook.quarter_summary`
  - dependency-linked EPIC concentration from `workbook.topic_map`
- UI placement: `Overview`
- Thresholds:
  - `High` = `>= 75`
  - `Medium` = `50–74`
  - `Low` = `< 50`

## Metric 5: PD-to-Revenue Efficiency

- Metric name: `PD to Revenue Efficiency`
- Business question: `Are we allocating engineering capacity to the highest-value revenue recovery bets?`
- Formula:
  - `Revenue unlock by quarter / PD in quarter`
  - show as `₹ Cr unlocked per 100 PD`
- Inputs:
  - `workbook.loss_intelligence`
  - `workbook.quarter_summary`
- UI placement: `Overview` or `AOP`
- Thresholds:
  - `High leverage` = `>= ₹1 Cr per 100 PD`
  - `Moderate leverage` = `₹0.4–1 Cr per 100 PD`
  - `Low leverage` = `< ₹0.4 Cr per 100 PD`

## Implementation Standard

- Every metric must trace to workbook-backed or source-backed data.
- If a metric is derived, the derivation rule must be deterministic and visible in code.
- No manually maintained status rollups.
- If a primary metric cannot be defended from source data, the dashboard should show insufficiency rather than false precision.
