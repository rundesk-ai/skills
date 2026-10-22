# UI performance and testing

Use this reference for UI budgets, invalidation, animation, pooling, Widget Components, Slate Insights,
functional input tests, screenshot comparison, or performance regressions.

## Establish the budget and workload

Measure a representative target/configuration, resolution, UI scale, input mode, culture, and worst-case live
content. Record UI thread time, paint/layout work, draw calls, live widgets, invalidations, textures, font
atlases, render targets, and memory where relevant. A quiet menu in PIE is not a HUD stress case.

Start with Widget Reflector to inspect hierarchy, focus, hit testing, clipping, culling, and obvious invalidation.
Use Slate Insights when a trace is needed to identify tick, active timer, repaint, volatility, or invalidation
reasons. Re-run the same capture after a change.

## Remove recurring work before caching it

1. Remove raw bindings, Blueprint Tick, unnecessary timers, and repeated tree searches.
2. Push bounded changes from events and update only affected widgets.
3. Collapse or remove unused screens and cap lists/notifications.
4. Use virtualized list views for large collections and reset every recycled entry before reuse.
5. Flatten needless hierarchy and prefer flow panels over nested Canvas/Overlay layers.
6. Measure again.
7. Add invalidation only around mostly static subtrees that now benefit.
8. Mark truly per-frame paint as volatile only after measuring the cache churn tradeoff.
9. Use a Retainer Panel only when reduced draw/repaint frequency repays its render-target memory and repaint cost.

Global invalidation and local Invalidation Boxes are alternate ownership strategies; do not stack them without
understanding which one is active. A frequently changing child can invalidate a large cached subtree.

## Keep animation and art inside budget

- Prefer opacity and render-transform animation to layout-changing properties.
- Do not animate large hierarchies when one small child or material parameter communicates the same change.
- Stop animations when a screen hides/deactivates and reset reusable widgets before replay.
- Avoid animation as the only state transition; tests and reduced-motion behavior need an immediate final state.
- Use textures instead of UI materials when no shader behavior is needed. Budget texture size, font atlases,
  material complexity, clipping, and layer breaks.
- Budget Widget Components at scale; see [world-space and specialized UI](world-space-and-specialized-ui.md).

## Test in layers

| Contract | Proof |
|---|---|
| Snapshot/model to display state | Engine-free or focused Automation test |
| UI action to validated command | Focused Automation test without pixel assertions |
| Screen open/close, modal, Back, and focus | Automation Driver or focused functional test; add device lanes beyond its documented desktop input |
| Layout, clipping, color, font, and animation | `AFunctionalUIScreenshotTest`, rendered comparison, and owner inspection |
| Navigation and input routing | Keyboard, mouse, gamepad, touch as applicable; Widget Reflector evidence |
| Performance budget | Repeatable Slate/Insights capture on a representative target |

Test initial, empty, loading, error, disabled, pending, rejected, and success states. Test rapid repeated input,
nested modal closure, focus-target removal, device change, travel/teardown, and two local players when supported.
Confirm the test filter discovers at least one intended test; a successful empty run is not proof.
