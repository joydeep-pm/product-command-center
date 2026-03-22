# Command Center Spec

## Purpose

The dashboard is a business operating console for the Finflux Core Lending platform. It is not only a visual artifact. It must help stakeholders answer:

- What is the current business problem?
- Which product gaps cost revenue?
- Which EPICs fix those gaps?
- What is planned by quarter?
- What is blocked by compliance, staffing, or dependencies?
- Which market bets are strategic versus immediate?
- Where is execution risk concentrated?

## Required views

1. Executive Snapshot
   - FY26 losses
   - Demo loss rate
   - Recoverable revenue
   - Total roadmap PD
   - EPIC count
   - new-market TAM

2. Strategic Imperatives
   - close the revenue bleed
   - pass the compliance firewall
   - enter new markets
   - use AI cautiously as differentiation
   - improve trust, quality, and loss prevention

3. Quarter-by-Quarter Roadmap
   - Q1 parity closure
   - Q2 enterprise readiness
   - Q3 B2B and international expansion
   - Q4 ecosystem monetization

4. EPIC Register
   - epic id
   - initiative name
   - quarter
   - category
   - PD
   - priority
   - business value
   - mapped loss linkage
   - competitor reference
   - dependency notes

5. Loss Intelligence
   - top lost deals
   - primary loss reasons
   - mapped EPIC recovery path
   - recovery priority

6. Competitive Parity
   - product family
   - feature group
   - Finflux status
   - competitor benchmark
   - gap severity
   - target fix quarter

7. Compliance and Risk
   - DPDPA
   - ECL
   - EIR
   - audit
   - provisioning
   - data residency
   - Shariah certification

8. Resource and Capacity Plan
   - PD by category and quarter
   - headcount implication
   - concentrated delivery risk

9. Dependencies and Constraints
   - domain SME dependencies
   - pod bandwidth conflicts
   - certification gates
   - implementation and trust risks

10. Source Index
   - deck
   - strategy report
   - roadmap PDF
   - roadmap workbook

## Canonical entities

- `epic`
- `loss_event`
- `competitive_benchmark`
- `resource_allocation`
- `dependency_edge`
- `executive_metric`
- `strategic_decision`

## First improvement priorities

1. Align the navigation labels and page sections to the source model above.
2. Make every headline metric traceable to a source section or data artifact.
3. Merge the top-loss view with the mapped EPIC fixes and target quarter.
4. Add a dedicated compliance and dependency surface so Q2 and Q3 execution risk is explicit.
5. Reduce any content that repeats without improving stakeholder decisions.
