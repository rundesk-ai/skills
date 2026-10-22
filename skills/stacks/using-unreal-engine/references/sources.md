# Unreal Engine 5.8 source map

Read this when choosing or auditing an engine API. These Epic pages are the UE 5.8 documentation; keep
the `application_version` parameter matched to the pinned engine when rechecking a contract.

| Guidance | Primary Epic source |
|---|---|
| Current engine changes and feature maturity | [UE 5.8 Release Notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes?application_version=5.8) |
| Epic's Unreal-specific C++ conventions | [C++ Coding Standard](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine?application_version=5.8) |
| Reflection metadata is editor-only | [Metadata Specifiers](https://dev.epicgames.com/documentation/en-us/unreal-engine/metadata-specifiers-in-unreal-engine?application_version=5.8) |
| `FName`, `FString`, and `FText` roles | [String Handling](https://dev.epicgames.com/documentation/en-us/unreal-engine/string-handling-in-unreal-engine?application_version=5.8) |
| `check`, `verify`, and `ensure` contracts | [Asserts](https://dev.epicgames.com/documentation/en-us/unreal-engine/asserts-in-unreal-engine?application_version=5.8) |
| Module structure, dependencies, and UBT build graph | [Unreal Engine Modules](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules?application_version=5.8) |
| Game, Client, Server, Editor, and Program target rules | [UBT Target Reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-build-tool-target-reference?application_version=5.8) |
| Debug, DebugGame, Development, Test, and Shipping behavior | [Build Configurations](https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configurations-reference-for-unreal-engine?application_version=5.8) |
| UBT invokes UHT before the compiler | [Unreal Header Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-header-tool-for-unreal-engine?application_version=5.8) |
| Reflected header format and UObject creation | [Objects](https://dev.epicgames.com/documentation/en-us/unreal-engine/objects-in-unreal-engine?application_version=5.8) |
| Header self-containment and IWYU | [Include What You Use](https://dev.epicgames.com/documentation/en-us/unreal-engine/include-what-you-use-iwyu-for-unreal-engine-programming?application_version=5.8) |
| Strong, weak, and soft UObject pointer behavior | [Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine?application_version=5.8) |
| Unreal shared pointers cannot own UObjects | [Smart Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-pointers-in-unreal-engine?application_version=5.8) |
| Gameplay framework roles and network reach | [Gameplay Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine?application_version=5.8) |
| Server-only rules and replicated match state | [Game Mode and Game State](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-mode-and-game-state-in-unreal-engine?application_version=5.8) |
| Engine-managed service lifetimes | [Programming Subsystems](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine?application_version=5.8) |
| Actor, Scene, and Primitive component roles | [Components](https://dev.epicgames.com/documentation/en-us/unreal-engine/components-in-unreal-engine?application_version=5.8) |
| Actor roles and composition | [Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/actors-in-unreal-engine?application_version=5.8) |
| Actor initialization and teardown | [Actor Lifecycle](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-actor-lifecycle?application_version=5.8) |
| Per-frame ordering, tick groups, and prerequisites | [Actor Ticking](https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine?application_version=5.8) |
| Delayed and periodic work | [Gameplay Timers](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-timers-in-unreal-engine?application_version=5.8) |
| Single-cast delegate safety and binding | [Delegates](https://dev.epicgames.com/documentation/en-us/unreal-engine/delegates-and-lambda-functions-in-unreal-engine?application_version=5.8) |
| Multicast delegate ordering | [Multicast Delegates](https://dev.epicgames.com/documentation/en-us/unreal-engine/multicast-delegates-in-unreal-engine?application_version=5.8) |
| Choosing C++ and Blueprint responsibilities | [Blueprint versus C++](https://dev.epicgames.com/documentation/en-us/unreal-engine/coding-in-unreal-engine-blueprint-vs-cplusplus?application_version=5.8) |
| Designing Blueprint-friendly C++ APIs | [Exposing C++ to Blueprints](https://dev.epicgames.com/documentation/en-us/unreal-engine/exposing-cplusplus-to-blueprints-visual-scripting-in-unreal-engine?application_version=5.8) |
| Reflection exposure specifiers and workflow | [Exposing Gameplay Elements](https://dev.epicgames.com/documentation/en-us/unreal-engine/exposing-gameplay-elements-to-blueprints-visual-scripting-in-unreal-engine?application_version=5.8) |
| Soft references and async loading lifetime | [Asynchronous Asset Loading](https://dev.epicgames.com/documentation/en-us/unreal-engine/asynchronous-asset-loading-in-unreal-engine?application_version=5.8) |
| Primary and secondary assets, bundles, and auditing | [Asset Management](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine?application_version=5.8) |
| Designer-authored Data Assets and Primary Data Assets | [Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine?application_version=5.8) |
| Querying unloaded asset metadata | [Asset Registry](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-registry-in-unreal-engine?application_version=5.8) |
| Editor validation for authored content | [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine?application_version=5.8) |
| Configuration categories, hierarchy, and overrides | [Configuration Files](https://dev.epicgames.com/documentation/en-us/unreal-engine/configuration-files-in-unreal-engine?application_version=5.8) |
| Project settings surface | [Project Settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/project-settings-in-unreal-engine?application_version=5.8) |
| Cross-session save objects and async saving | [Saving and Loading](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine?application_version=5.8) |
| GUID-based versions for custom serialization | [Versioning Assets and Packages](https://dev.epicgames.com/documentation/en-us/unreal-engine/versioning-of-assets-and-packages-in-unreal-engine?application_version=5.8) |
| Safe reflected symbol and package renames | [Core Redirects](https://dev.epicgames.com/documentation/en-us/unreal-engine/core-redirects-in-unreal-engine?application_version=5.8) |
| Asset moves, redirectors, and referencer repair | [Asset Redirectors](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-redirectors-in-unreal-engine?application_version=5.8) |
| Game-thread and parallel-processing cautions | [Common Memory and CPU Performance Considerations](https://dev.epicgames.com/documentation/en-us/unreal-engine/common-memory-and-cpu-performance-considerations-in-unreal-engine?application_version=5.8) |
| Live Coding object reinstancing | [Live Coding](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-live-coding-to-recompile-unreal-engine-applications-at-runtime?application_version=5.8) |
| Server authority and replication system choices | [Networking Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine?application_version=5.8) |
| Durable property replication and RepNotify | [Replicate Actor Properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/replicate-actor-properties-in-unreal-engine?application_version=5.8) |
| RPC direction, ownership, and execution | [Remote Procedure Calls](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine?application_version=5.8) |
| Actor ownership and owning-connection rules | [Actor Owner and Owning Connection](https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-owner-and-owning-connection-in-unreal-engine?application_version=5.8) |
| Replication and RepNotify ordering guarantees | [Replicated Object Execution Order](https://dev.epicgames.com/documentation/en-us/unreal-engine/replicated-object-execution-order-in-unreal-engine?application_version=5.8) |
| Replicated component and subobject behavior | [Actor Component Replication](https://dev.epicgames.com/documentation/en-us/unreal-engine/replicating-actor-components-in-unreal-engine?application_version=5.8) |
| Alternate large-scale replication architecture | [Replication Graph](https://dev.epicgames.com/documentation/en-us/unreal-engine/replication-graph-in-unreal-engine?application_version=5.8) |
| Opt-in Iris architecture and configuration | [Introduction to Iris](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-iris-in-unreal-engine?application_version=5.8) |
| Iris migration differences | [Migrate to Iris](https://dev.epicgames.com/documentation/en-us/unreal-engine/migrate-to-iris-in-unreal-engine?application_version=5.8) |
| Structured runtime logging | [Logging](https://dev.epicgames.com/documentation/en-us/unreal-engine/logging-in-unreal-engine?application_version=5.8) |
| Spatial gameplay history | [Visual Logger](https://dev.epicgames.com/documentation/en-us/unreal-engine/visual-logger-in-unreal-engine?application_version=5.8) |
| Quick runtime performance triage | [Stat Commands](https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine?application_version=5.8) |
| Choosing Stats, Insights, or a frame debugger | [Performance Profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine?application_version=5.8) |
| Timing, memory, and loading traces | [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine?application_version=5.8) |
| Order-independent, self-cleaning Automation tests | [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine?application_version=5.8) |
| Command-line test execution | [Run Automation Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine?application_version=5.8) |
| Multi-process and packaged-session automation | [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine?application_version=5.8) |
| Running Gauntlet sessions | [Running Gauntlet Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine?application_version=5.8) |
| Build, cook, stage, package, deploy, and run boundaries | [Build Operations](https://dev.epicgames.com/documentation/en-us/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine?application_version=5.8) |
| Packaging concepts and platform prerequisites | [Packaging Projects](https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project?application_version=5.8) |
| Plugin structure, module types, and loading phases | [Plugins](https://dev.epicgames.com/documentation/en-us/unreal-engine/plugins-in-unreal-engine?application_version=5.8) |
| Engine-version migration workflow | [Updating Projects](https://dev.epicgames.com/documentation/en-us/unreal-engine/updating-projects-to-newer-versions-of-unreal-engine?application_version=5.8) |

Epic's documentation is a live source and some 5.8 pages retain older examples. Confirm signatures
against the installed engine headers. Any engine-free architecture seam and visual sign-off rule
come from the host repository, not from Epic.
