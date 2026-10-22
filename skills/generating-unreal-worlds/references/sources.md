# Unreal world-generation source map

Read this before adopting or changing Landscape, PCG, World Partition, builder commandlets, validation, or
navigation behavior. Links are Epic's UE 5.8 documentation.

| Guidance | Primary Epic source | Limit |
|---|---|---|
| Landscape dimensions, components, sections, and performance | [Landscape Technical Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-technical-guide-in-unreal-engine?application_version=5.8) | Valid sizes and workload must be measured for the host game |
| Landscape and World Partition integration | [Landscape Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-overview?application_version=5.8) | Streaming is a separate adoption decision |
| World Partition model and conversion commandlet | [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine?application_version=5.8) | Conversion documents report-only mode and unstable GUID risk |
| Runtime PCG scheduling and generation sources | [Using PCG Generation Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-pcg-generation-modes-in-unreal-engine?application_version=5.8) | Execution order is not a semantic contract |
| PCG Biome Core and Sample maturity | [PCG Biome](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-pcg-biome-core-and-sample-plugins-in-unreal-engine?application_version=5.8) | Experimental in UE 5.8; verify before adoption |
| PCG component seed | [UPCGComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCG/UPCGComponent?application_version=5.8) | No general cross-platform identity guarantee |
| PCG point seed | [FPCGPoint](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCG/FPCGPoint?application_version=5.8) | No general cross-platform identity guarantee |
| PCG editor determinism test surface | [FPCGEditor](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCGEditor/FPCGEditor?application_version=5.8) | Supplement with project invariants |
| Builder commandlets for HLOD, navmesh, and PCG | [World Partition Builder Commandlet Reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-builder-commandlet-reference?application_version=5.8) | Relevant only if those systems are adopted |
| Custom and command-line asset validation | [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine?application_version=5.8) | Check plugin state first |
| Navigation precision and generation-cost tradeoff | [Optimizing Navigation Mesh Generation Speed](https://dev.epicgames.com/documentation/en-us/unreal-engine/optimizing-navigation-mesh-generation-speed-in-unreal-engine?application_version=5.8) | Profile representative workloads |
| World Partition navmesh modes | [World Partitioned Navigation Mesh](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partitioned-navigation-mesh?application_version=5.8) | Experimental in UE 5.8 |
| UE 5.8 PCG and world changes | [Unreal Engine 5.8 Release Notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes) | Recheck status before adoption |

The semantic-record seam, normalized determinism manifest, approved asset provenance, and visual
handoff come from the host repository's rules and requirements.
