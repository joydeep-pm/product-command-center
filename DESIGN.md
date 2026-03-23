# Design System — M2P Finflux Product Command Center

## Product Context
- **What this is:** A live internal command center for the Finflux Core Lending platform. It helps product, GTM, and leadership teams see execution posture, revenue unlocks, parity gaps, compliance blockers, and quarter risk in one place.
- **Who it's for:** Product leadership, business leadership, GTM stakeholders, and the wider internal stakeholder group that needs live, trusted status rather than local spreadsheets or deck snapshots.
- **Space/industry:** Digital lending, loan management systems, core lending operations, internal command-center software.
- **Project type:** Shared internal web application / business operating dashboard.

## Aesthetic Direction
- **Direction:** Refined industrial operating room
- **Decoration level:** Intentional
- **Mood:** Calm, exacting, executive, and high-trust. It should feel like a room where serious product and business decisions get made, not a startup analytics toy and not a glossy presentation layer.
- **Reference sites:** Internal product context only. No external design research was used for this initial system.

## Typography
- **Primary heading system:** `Satoshi` — use this for page titles, section titles, thesis blocks, major metrics, and all operational emphasis. It reads sharper, more technical, and more native to a product command center than an editorial serif.
- **Body:** `Satoshi` — highly legible, understated, and strong at medium-density operational reading.
- **UI/Labels:** `Satoshi` — use semibold weights and tracking shifts for hierarchy rather than introducing a contrasting display family.
- **Data/Tables:** `Satoshi` — crisp numerals and stronger technical character for tables, filters, matrices, and dense metric rows.
- **Code:** `IBM Plex Mono`
- **Loading:** Fontshare for `Satoshi`; `IBM Plex Mono` is optional for code-like IDs and traces only
- **Scale:**
  - `12px` micro metadata only
  - `14px` secondary labels and compact controls
  - `16px` default body and table text
  - `18px` dense card titles and topbar labels
  - `22px` section titles
  - `30px` primary metrics
  - `40px` executive hero numbers only

## Color
- **Approach:** Restrained
- **Primary:** `#2F6BFF` — live operational emphasis, active filters, links, progress, and selected navigation
- **Secondary:** `#C8922E` — strategic attention, caution, and executive emphasis; use sparingly
- **Neutrals:** Cool slate range
  - `#04101C` page background
  - `#0B1726` surface
  - `#112134` card
  - `#1D3047` raised card / active utility surface
  - `#314966` border
  - `#93A8C3` muted text
  - `#D9E3F0` primary text
- **Semantic:** success `#1F9D68`, warning `#D98E04`, error `#D64545`, info `#3483FA`
- **Dark mode:** Primary mode. Surfaces stay deep and cool; accents should not be oversaturated. Light mode is a functional alternate, not the hero expression of the brand.

## Spacing
- **Base unit:** `8px`
- **Density:** Comfortable-compact
- **Scale:** `2xs(4)` `xs(8)` `sm(12)` `md(16)` `lg(24)` `xl(32)` `2xl(48)` `3xl(64)`

## Layout
- **Approach:** Grid-disciplined with selective editorial emphasis
- **Grid:** 12-column desktop logic; 6-column tablet; 1-column mobile stacking for priority content
- **Max content width:** Use full-bleed shell for app chrome, but keep dense reading zones within roughly `1440px`
- **Border radius:** `sm 6px`, `md 10px`, `lg 14px`, `pill 999px`

## Motion
- **Approach:** Minimal-functional
- **Easing:** enter `cubic-bezier(0.2, 0.8, 0.2, 1)`, exit `ease-in`, move `ease-in-out`
- **Duration:** micro `80ms`, short `160ms`, medium `240ms`, long `360ms`

## System Rules
- Viewer mode must feel materially cleaner than editor mode. Editing affordances should recede unless the user explicitly unlocks editing.
- Overview is an executive scan surface first. Operational detail belongs behind folds, filters, or secondary panes.
- Do not use editorial serif display typography in the live dashboard. This product is a high-trust operating surface, not a magazine layout or strategy deck cover.
- Keep the heading system sans-first across Overview, Strategy, Roadmap, Risks, AOP, and Deep-Dives. Hierarchy should come from weight, spacing, and composition, not from switching to a decorative font.
- Do not use purple as a primary accent. Reserve color for meaning, not decoration.
- Avoid gradient-heavy or marketing-style hero treatments. This product earns trust through precision and restraint.
- Every high-value metric should visually read as source-backed and decision-relevant, not as dashboard filler.
- Tables, filters, and chips must be readable at normal laptop zoom without squinting.

## Implementation Guidance
- Promote recency, owner, and status signals into clear structured blocks rather than scattered metadata text.
- Reduce simultaneous topbar controls. If a control is not relevant to a viewer, hide or demote it.
- Make hierarchy more obvious between:
  - executive metrics
  - quarter execution signals
  - supporting operational detail
- Prefer fewer, larger cards over many small equally weighted cards on Overview.
- Audit deeper panes against the same standard: hierarchy first, density second, chrome last.

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-23 | Initial design system created | Grounded in the command-center requirements, current dashboard shell, and the stated identity: high-trust internal operating room for product and business leadership |
