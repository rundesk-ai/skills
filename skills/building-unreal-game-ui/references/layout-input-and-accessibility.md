# Layout, input, and accessibility

Use this reference for responsive layout, localization, fonts, focus, navigation, input modes, cursor
capture, safe zones, or accessibility behavior.

## Build layouts that adapt

- Establish a reference resolution and author at DPI scale 1.0. Use the declared DPI curve for runtime scale.
- Use flow panels, padding, alignment, minimum/maximum constraints, and size boxes before fixed coordinates.
- In a Canvas Panel, anchors describe the relationship to the parent; offsets then describe margins or size.
  Test each supported aspect ratio instead of assuming anchors make a layout responsive.
- Put critical edge UI inside a Safe Zone. Preview device profiles, orientation, and debug safe zones, then
  verify on a representative device or platform build.
- Use render transforms for temporary animation, not permanent layout; they do not participate in layout.
- Test long values, zero, maximum magnitude, missing data, wrapped text, right-to-left layout, and font fallback.

## Treat screen entry and exit as input transactions

Opening an interactive screen must establish, as one coherent policy:

- Game Only, Game and UI, or UI Only input mode;
- initial focus and keyboard/gamepad navigation;
- cursor visibility, capture, confinement, and hover behavior;
- gameplay movement/look suppression;
- UI and gameplay mapping-context priority;
- pause and time-dilation behavior; and
- Back/Escape, cancel, confirm, modal, and focus-restoration semantics.

Closing restores the previous valid policy even after travel, controller disconnect, forced teardown, failed
commands, or nested modal closure. Avoid several widgets independently changing PlayerController input state.

Add and remove UI mapping contexts symmetrically through the owning local player's Enhanced Input subsystem.
Keep gameplay and UI contexts distinct, assign their priority intentionally, and do not let an inactive leaf
widget retain a context. Prefer player-specific user focus to global keyboard focus when multiple local users
are possible.

For directional navigation, test every focusable control with keyboard and gamepad. Set explicit navigation
at irregular layouts and boundaries; define wrap, stop, or escape intentionally. Maintain one clear visible
focus target. Pointer hover and keyboard/gamepad focus are distinct states and must not create contradictory UI.

## Make text localizable and robust

- Use `FText` for player-facing text and preserve its text history. Use culture-aware formatting for numbers,
  percentages, currency, dates, times, and plurals.
- Use format patterns with named arguments. Do not build sentences by concatenating translated fragments.
- Use string tables when a shared body of authored text needs stable keys and centralized reuse; do not
  replace clear local `LOCTEXT` literals with a table solely for uniformity.
- Use culture-invariant text only for genuinely non-localized values such as an external player name.
- Use Composite Fonts with fallback families for every supported script. Test glyph coverage, shaping,
  wrapping, line height, and memory/loading policy.
- Exercise pseudo-localization or representative long translations early, not only after layout is complete.

## Preserve meaning across abilities and preferences

- Never encode critical state only with color, shape, sound, hover, motion, or spatial position. Combine cues.
- Keep text readable over changing world backgrounds; give HUD text sufficient contrast and a stable backing.
- Keep focus visible and navigation complete without a pointer. Give controls useful accessible names and
  summaries where the selected platform surface supports them.
- Support the declared UI scale, subtitle/text preferences, reduced-motion behavior, and remapped controls.
- Do not make animation delay input or hide state longer than its semantic transition requires.
- Treat screen-reader and text-to-speech support as version- and platform-sensitive; verify the actual target.
