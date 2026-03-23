# Lessons

- For this repo, optimize for stakeholder usefulness, not just visual polish. Every dashboard change should improve business visibility across strategy, roadmap, losses, parity, risks, and operating dependencies.
- Keep the mutation surface small. Prefer improving `/Users/joy/autoresearch/app/dashboard.html` while keeping extraction, evaluation, and source-of-truth data separate.
- Before claiming progress, verify both content coverage and render quality. A pretty dashboard with missing source coverage is a regression.
- Do not trust liberal evaluators. If a score is mostly driven by keyword presence or broad structure checks, treat it as weak evidence and tighten the rubric before using it to guide iterations.
- Do not confuse analytical structure with research depth. For market-research work, depth means explicit methodology, quantified coverage, named-player breadth, and honest completeness gaps, not just solid synthesis and a clean narrative.
- For this dashboard, QA cannot stop at “no console errors” or “navigation works.” It must explicitly check executive density, type legibility, protected-view hydration state, topbar wrapping, and badge clipping on both desktop and mobile.
- When dashboard panes are source-hydrated or data-sparse in static previews, verify the typography layer separately from content completeness. Readability fixes still need proof even if the pane preview cannot fully render business data.
- When shell controls behave inconsistently across breakpoints, check for CSS component-name collisions before adjusting spacing. Reusing a class like `status-chip` for both header state chips and tiny inline pills caused the “Updated by” block to wrap and degrade unpredictably.
- Do not harden temporary access-control assumptions into the product without rechecking the operating model. For this dashboard, internal read access is intentionally open while live writes alone need protection.
- Treat `vercel dev` as production-adjacent when Blob credentials are present. Shared-state write tests can mutate the live store unless storage is isolated first or the prior state is restored immediately after verification.
- Do not reuse the overview’s serif display title style inside operational panes like Roadmap. Pane thesis blocks should read like decision support, not like editorial poster copy.
