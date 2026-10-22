# Unreal game UI source map

Read this when choosing or auditing a version-sensitive UI behavior. Links are Epic's UE 5.8 documentation;
match `application_version` to the pinned engine when rechecking.

| Guidance | Primary Epic source | Limit |
|---|---|---|
| UMG C++ data object, C++ widget API, and Widget Blueprint composition pattern | [Epic UMG Best Practices tech blog](https://www.unrealengine.com/tech-blog/umg-best-practices) | Architecture example, not an engine requirement |
| Data-driven construction for changing interface content | [Creating a Data-Driven UI with UMG](https://www.unrealengine.com/tech-blog/creating-a-data-driven-ui-with-umg?lang=en-US) | Adapt the pattern to typed domain data |
| Player-specific viewport creation and input modes | [Creating Widgets](https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-widgets-in-unreal-engine?application_version=5.8) | Tutorial ownership examples are illustrative, not defaults |
| HUD, menus, Canvas, UMG, and Slate roles | [User Interfaces and HUDs](https://dev.epicgames.com/documentation/en-us/unreal-engine/user-interfaces-and-huds-in-unreal-engine?application_version=5.8) | Prefer UMG unless a lower-level need is proved |
| `UUserWidget` API surface | [`UUserWidget`](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/UMG/UUserWidget?application_version=5.8) | Verify signatures in installed headers |
| C++ versus Blueprint responsibilities | [Blueprint versus C++](https://dev.epicgames.com/documentation/en-us/unreal-engine/coding-in-unreal-engine-blueprint-vs-cplusplus?application_version=5.8) | Choose by lifetime and testability |
| One-time `UUserWidget` initialization | [`OnInitialized`](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/UMG/UUserWidget/OnInitialized?application_version=5.8) | Construct/Destruct can still repeat |
| Required and optional Widget Designer child contracts | [`BindWidget` metadata](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/UMG/UMWidget_1?application_version=5.8) | Required names are serialized authoring contracts |
| Player-scoped screen attachment | [`AddToPlayerScreen`](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/UserInterface/Viewport/AddtoPlayerScreen?application_version=5.8) | Prefer over global viewport attachment for local-player UI |
| Widget reuse and pooling mechanics | [`FUserWidgetPool`](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/UMG/FUserWidgetPool?application_version=5.8) | Recycled entries require full reset |
| Layout, art, reuse, transforms, and event-driven authoring | [UMG Best Practices](https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-best-practices-in-unreal-engine?application_version=5.8) | Measure the actual target |
| Event-driven UMG updates instead of raw bindings | [Optimization Guidelines for UMG](https://dev.epicgames.com/documentation/en-us/unreal-engine/optimization-guidelines-for-umg-in-unreal-engine?application_version=5.8) | Measure the actual target workload |
| Enforcing Widget Designer authoring rules | [Widget Designer Team Settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/widget-designer-team-settings-in-the-unreal-engine-project-settings?application_version=5.8) | Adopt only rules the team can maintain |
| Invalidation and Retainer Panel tradeoffs | [Invalidation in Slate and UMG](https://dev.epicgames.com/documentation/en-us/unreal-engine/invalidation-in-slate-and-umg-for-unreal-engine?application_version=5.8) | Retainers add memory and repaint cost |
| Widget hierarchy, focus, clipping, hit tests, and navigation inspection | [Widget Reflector](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-slate-widget-reflector-in-unreal-engine?application_version=5.8) | PIE/Standalone snapshot limitations apply |
| Slate focus, input, paint, and invalidation event diagnostics | [Console Slate Debugger](https://dev.epicgames.com/documentation/en-us/unreal-engine/console-slate-debugger-in-unreal-engine?application_version=5.8) | Use bounded filters; avoid log floods |
| Slate layout passes, attributes, polling, and live-widget cost | [Slate Architecture](https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-slate-ui-architecture-in-unreal-engine?application_version=5.8) | Low-level mechanics; verify headers for exact API |
| CommonUI fit for layered and cross-platform interfaces | [CommonUI Design Guidelines](https://dev.epicgames.com/documentation/en-us/unreal-engine/design-guidelines-for-using-commonui-in-unreal-engine?application_version=5.8) | Epic gives a PC-only RTS as a likely non-fit |
| CommonUI core maturity in UE 5.8 | [UE 5.8 Release Notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes?application_version=5.8) | Enhanced Input integration has a separate caution |
| Activatable widget stacks | [`UCommonActivatableWidgetStack`](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/CommonUI/UCommonActivatableWidgetStack?application_version=5.8) | Push through the stack, never also to the viewport |
| CommonUI activation trees and layered routing | [CommonUI Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-advanced-multiplatform-user-interfaces-with-common-ui-for-unreal-engine?application_version=5.8) | Not every widget should be activatable |
| CommonUI viewport routing and action tables | [Common UI Quickstart](https://dev.epicgames.com/documentation/en-us/unreal-engine/common-ui-quickstart-guide-for-unreal-engine?application_version=5.8) | Plugin adoption requires project approval |
| CommonUI input-mode behavior and restoration | [Input Fundamentals for CommonUI](https://dev.epicgames.com/documentation/en-us/unreal-engine/input-fundamentals-for-commonui-in-unreal-engine?application_version=5.8) | Do not mix competing input-config owners |
| CommonUI and Enhanced Input integration | [Using CommonUI With Enhanced Input](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-commonui-with-enhnaced-input-in-unreal-engine?application_version=5.8) | Page retains an older maturity caution; verify locally |
| Game-and-UI input mode | [Set Input Mode Game and UI](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Input/SetInputModeGameAndUI?application_version=5.8) | One owner applies and restores it |
| Base Enhanced Input contexts and local-player subsystem | [Enhanced Input](https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine?application_version=5.8) | Add and remove UI contexts symmetrically |
| UMG MVVM setup and field notifications | [UMG Viewmodel](https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-viewmodel-for-unreal-engine?application_version=5.8) | Beta and plugin-gated in UE 5.8 |
| Resolution-independent scaling | [DPI Scaling](https://dev.epicgames.com/documentation/en-us/unreal-engine/dpi-scaling-in-unreal-engine?application_version=5.8) | Test the project's supported resolutions |
| Responsive Canvas relationships | [UMG Anchors](https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-anchors-in-unreal-engine-ui?application_version=5.8) | Anchors do not replace aspect-ratio testing |
| Device safe zones | [UMG Safe Zones](https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-safe-zones-in-unreal-engine?application_version=5.8) | Preview and real-device evidence differ |
| Localizable user-facing text | [Text Localization](https://dev.epicgames.com/documentation/en-us/unreal-engine/text-localization-in-unreal-engine?application_version=5.8) | Use `FText` for display text |
| Stable shared localized text keys | [String Tables](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-string-tables-for-text-in-unreal-engine?application_version=5.8) | Use when central reuse earns indirection |
| Culture data, fallbacks, formatting, and bidirectional text | [Localization Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/localization-overview-for-unreal-engine?application_version=5.8) | Package only required culture data |
| Composite fonts, glyph fallbacks, loading, and layout metrics | [Font Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/font-asset-and-editor-in-unreal-engine?application_version=5.8) | Test every supported script |
| Font-point to Slate-unit scaling | [Font DPI Scaling](https://dev.epicgames.com/documentation/en-us/unreal-engine/font-dpi-scaling-in-unreal-engine?application_version=5.8) | Choose the compatibility policy early |
| UI accessibility tool surface | [Designing UI for Accessibility](https://dev.epicgames.com/documentation/en-us/unreal-engine/designing-ui-for-accessibility-in-unreal-engine?application_version=5.8) | Platform support varies |
| Widget tick, timer, repaint, and invalidation evidence | [Slate Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-insights-in-unreal-engine?application_version=5.8) | Check plugin state and approval first |
| Widget Blueprint animation tracks and playback | [Animating UMG Widgets](https://dev.epicgames.com/documentation/en-us/unreal-engine/animating-umg-widgets-in-unreal-engine?application_version=5.8) | Prefer transforms/opacity and measure invalidation |
| Automation interfaces including input and screenshot testing | [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine?application_version=5.8) | Enable only approved test plugins |
| Desktop pointer and keyboard interaction automation | [Automation Driver](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine?application_version=5.8) | Do not infer gamepad or touch coverage |
| Command-line test execution | [Run Automation Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine?application_version=5.8) | Confirm non-zero discovery |
| Rendered screenshot comparison | [Screenshot Comparison Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine?application_version=5.8) | Requires a rendered test lane |
| UI-inclusive functional screenshot surface | [`AFunctionalUIScreenshotTest`](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Developer/FunctionalTesting/AFunctionalUIScreenshotTest?application_version=5.8) | Ordinary automation screenshots exclude UI |
| Ordinary automation screenshot limitation | [`TakeAutomationScreenshot`](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Automation/TakeAutomationScreenshot?application_version=5.8) | Explicitly does not capture UI |
| UMG and Slate screen-reader surface | [Supporting Screen Readers](https://dev.epicgames.com/documentation/en-us/unreal-engine/supporting-screen-readers-in-unreal-engine?application_version=5.8) | Experimental and platform-limited |
| Render-target-backed in-world UMG | [Widget Components](https://dev.epicgames.com/documentation/en-us/unreal-engine/widget-components-in-unreal-engine?application_version=5.8) | Budget redraw and render-target memory |
| Simulated pointer interaction with world widgets | [Widget Interaction Components](https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-widget-interaction-components-in-unreal-engine?application_version=5.8) | Keep virtual user and pointer IDs distinct |
| Drag visual and payload mechanics | [Creating Drag-and-Drop UI](https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-drag-and-drop-ui-in-unreal-engine?application_version=5.8) | Authoritative validation still belongs outside the widget |

## Implementation studies and talks

These sources add production patterns and source-reading context. They are not substitutes for the
installed engine headers, an enabled plugin's source, or measured behavior.

| Topic | Source | Use |
|---|---|---|
| Modular sample with UMG HUDs and CommonUI | [Epic Lyra Sample Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine?application_version=5.8) | Study concepts; do not copy the whole architecture |
| Lyra local-player layout and named layer stacks | [X157 Lyra UI Policy analysis](https://x157.github.io/UE5/LyraStarterGame/CommonUI/DefaultUIPolicy.html) | Community analysis; confirm against the matching sample version |
| Lyra HUD, menu, modal, and CommonUI input setup | [X157 Lyra CommonUI analysis](https://x157.github.io/UE5/LyraStarterGame/CommonUI/) | Community analysis; version-sensitive |
| UMG/Slate lifecycle, visibility, focus, split-screen, and world-widget mechanics | [UMG/Slate Compendium](https://github.com/YawLighthouse/UMG-Slate-Compendium) | Deep community reference; verify current APIs |
| UI frame cost and advanced rendering tradeoffs | [Optimizing and Building UI for AAA Games](https://www.youtube.com/watch?v=OyY3OYbNK7s) | Epic Unreal Fest talk; profile before adopting advanced techniques |

The state-to-view seam, semantic-action boundary, vocabulary, and visual handoff come from the host
repository's contracts, not from Unreal itself.
