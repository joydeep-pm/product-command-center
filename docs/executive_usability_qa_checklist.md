# Executive Usability QA Checklist

Use this before calling the dashboard ready for stakeholder review. This checklist is intentionally separate from functional QA.

## 1. Density
- Above the fold answers the top question without requiring expansion or scrolling.
- Secondary controls, matrices, and evidence blocks are collapsed or visually de-emphasized by default.
- No single pane opens with more than two dense grids competing for attention.

## 2. Type
- Primary headings are readable at normal laptop viewing distance without zoom.
- Supporting copy is readable on both desktop and mobile without squinting.
- Table headers, filter labels, pills, and row metadata are still legible at 100% browser zoom.
- Muted text is subdued, not faint.

## 3. Protected Viewer State
- Re-check the page after the protected/shared state hydrates, not just the initial HTML.
- Verify topbar mode, timestamp, actor, and badges after hydration.
- Verify no shell element clips, wraps awkwardly, or jumps after live data loads.

## 4. Mobile
- Topbar status values stack cleanly on narrow screens.
- Action buttons do not collide with badges.
- No value chips or labels truncate unexpectedly.
- Filter bars wrap into usable rows instead of compressed one-line strips.

## 5. Executive Scan Test
- A stakeholder can explain the page's main message in under 30 seconds.
- The most important metric or decision cue is visually dominant.
- Supporting evidence exists, but does not overpower the main story.

## 6. Pane-Specific Checks
### Overview
- Secondary operational surfaces are not forced open by default.
- Status controls are easy to reach when needed, invisible when not.

### Strategy
- Narrative blocks have enough spacing to read as guidance, not as data tables.
- Comparative tables do not overpower the strategic argument.

### Roadmap
- Quarter and status controls remain legible at a glance.
- EPIC cards remain readable without opening each item.

### AOP
- Table headers, IDs, and row names remain readable without zoom.
- Summary metrics above the table are scannable before the table itself.

### Risks & Hiring
- Risk descriptions are readable in one pass.
- Decision and hiring rows do not look like dense admin logs.

### Product Deep-Dives
- Section labels and product cards are readable before opening the full panel.
- Deep-dive metadata reads as a product summary, not debug info.

## 7. Failure Conditions
If any of these are true, the page is not ready:
- A stakeholder says "too much information" on first view.
- A key label, badge, or timestamp wraps/clips awkwardly.
- Important text is technically visible but uncomfortable to read.
- The page passes functional QA but fails the 30-second executive scan test.
