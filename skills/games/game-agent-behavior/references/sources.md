# Game agent behavior source map

Use this file to audit a rule, not as more procedure. Every source below was opened on 2026-10-25.
The pseudocode is written fresh from the contracts the sources describe; no listing is copied.

## Think/act split and arbitration

- Jeff Orkin,
  [Three States and a Plan: The A.I. of F.E.A.R.](https://pages.cs.wisc.edu/~dyer/cs540/handouts/gdc2006_orkin_jeff_fear.pdf)
  (GDC 2006; a university mirror of the paper).
  - A three-state machine (Goto, Animate, UseSmartObject), with every choice made by a planner.
  - The planner runs A* over a fixed-size world-state array, with a cost per action and procedural
    preconditions.
- Tomasz Zubek,
  [1000 NPCs at 60 FPS](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter34_1000_NPCs_at_60_FPS.pdf)
  (Game AI Pro 3; Project Highrise).
  - An action queue that re-selects only when empty: "the system only evaluates the world when it has
    nothing to do".
  - Failure monitoring, with a flush and a fallback, and schedule blocks.
  - NPCs simulated continuously rather than culled.
  - The needs model was removed as hidden information.
- Robert Zubek, [Needs-Based AI](https://robert.zubek.net/publications/Needs-based-AI-draft.pdf)
  (draft of a Game Programming Gems 8 chapter). A Sims-lineage account, not Maxis documentation.
  - Selection when actions run out.
  - Attenuated need-delta scoring, against raw sums.
  - Distance in the score as "bird in hand".
  - Rewards granted by the action, so that interrupted actions are not rewarded.
  - False advertising creating loops.
  - Intermediate results left in the world, and thought bubbles for players.
- Shining Rock Software, [Game Code Design](https://shiningrocksoftware.com/2018-11-09-game-code-design/)
  (2018). Decisions spread across composed state machines broke old behaviour whenever a new need was
  added.
- Bay 12 Games, [DF Talk 22 transcript](https://bay12games.com/media/df_talk_22_transcript.html).
  - Jobs picking workers snatch the nearest qualified dwarf; workers picking jobs take work another
    would do better.
  - A merging layer with a delay is needed.
  - These are statements of plans, not a shipped mechanism.
- [Q&A: Dissecting the development of Dwarf Fortress](https://www.gamedeveloper.com/design/q-a-dissecting-the-development-of-i-dwarf-fortress-i-with-creator-tarn-adams)
  (Game Developer, 2019). Job assignment every 100 ticks, with job applications staggered from it.
- Dragon Age: Inquisition,
  [Behavior Decision System](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter31_Behavior_Decision_System_Dragon_Age_Inquisition%E2%80%99s_Utility_Scoring_Architecture.pdf)
  (Game AI Pro 3). Continuous re-evaluation, suspended after an ability executes; fixed score bands per
  behaviour class; evaluation results kept in a debug table.

## Architectures

- [Behavior Selection Algorithms](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter04_Behavior_Selection_Algorithms.pdf)
  (Game AI Pro). A survey of state machines, behaviour trees, utility, goal planning and HTN.
  - State machines become hard to extend at tens of states.
  - Stateless behaviours loop a citizen between two behaviours.
- [A Reusable, Light-Weight Finite-State Machine](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter12_A_Reusable_Light-Weight_Finite-State_Machine.pdf)
  (Game AI Pro 3). State instances live as long as the machine, so they reset in enter and exit; shared
  state objects.
- Champandard and Dunstan,
  [The Behavior Tree Starter Kit](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter06_The_Behavior_Tree_Starter_Kit.pdf)
  (Game AI Pro).
  - Initialise once before the first update, then update, then terminate once.
  - The tick wrapper; abort and the ABORTED status.
  - An active selector that aborts the previously running child.
  - Shared nodes with per-agent tasks; an event-driven scheduler with suspended leaves.
- BehaviorTree.CPP, [Sequence nodes](https://www.behaviortree.dev/docs/nodes-library/SequenceNode) and
  [the sequence tutorial](https://www.behaviortree.dev/docs/tutorial-basics/tutorial_04_sequence) (v4).
  Sequence against reactive sequence; stateful actions with `onStart`, `onRunning` and `onHalted`,
  aborted as fast as possible when halted.
- py_trees, [Behaviours](https://py-trees.readthedocs.io/en/devel/behaviours.html). Terminate is called
  on every switch to a non-running state; INVALID means a higher-priority branch interrupted.
- Unreal Engine,
  [Behavior Tree overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview),
  [decorator reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-behavior-tree-node-reference-decorators),
  and [State Tree overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine).
  - Behaviour trees are event-driven.
  - Observer aborts: none, self, lower priority, both.
  - State Tree combines behaviour-tree selectors with state-machine transitions.
- LimboAI, [discussion #143](https://github.com/limbonaut/limboai/discussions/143) (2024). A plain
  selector resumes the running action without rechecking the condition. A community source.
- Troy Humphreys,
  [Exploring HTN Planners through Example](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter12_Exploring_HTN_Planners_through_Example.pdf)
  (Game AI Pro).
  - The conditions that force a replan.
  - The bug where a task's own effect triggers a replan.
  - Accepting a replan only through the method traversal record, which also stops a replan aborting a
    still-valid task.
- [Fluid HTN](https://github.com/ptrefall/fluid-hierarchical-task-network) (MIT). Replans only on
  completion, failure or a world change, and rejects early any replan that cannot win.
- Eric Jacopin,
  [Optimizing Practical Planning for Game AI](https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter13_Optimizing_Practical_Planning_for_Game_AI.pdf)
  (Game AI Pro 2). Under one plan per second per NPC, plans of at most four actions, at most several ms.
- [Structural Architecture: Common Tricks of the Trade](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter05_Structural_Architecture_Common_Tricks_of_the_Trade.pdf)
  (Game AI Pro). Inertia and cooldowns; reserving cover on a blackboard; smart objects and hotspots.
- [Smart Zones](https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter11_Smart_Zones_to_Create_the_Ambience_of_Life.pdf)
  (Game AI Pro 2) and
  [Ambient Interactions](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter35_Ambient_Interactions_Improving_Believability_by_Leveraging_Rule-Based_AI.pdf)
  (Game AI Pro 3). Role slots and cardinality; a scene does not start without its main roles; reserve
  the seat when the action is committed.
- [Breathing Life into Your Background Characters](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter36_Breathing_Life_into_Your_Background_Characters.pdf)
  (Game AI Pro). Schedules as a hierarchical state machine keyed by time; the schedule asked when idle;
  Gaussian jitter on schedule update times.

## Utility scoring

- Mike Lewis,
  [Choosing Effective Utility-Based Considerations](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter13_Choosing_Effective_Utility-Based_Considerations.pdf)
  (Game AI Pro 3; Guild Wars 2: Heart of Thorns).
  - Bookends and normalisation; multiplied considerations with a veto at zero.
  - The cheap-first order, with the raycast last for performance.
  - A commitment bonus only shifts where scores land; adding a separating consideration is the fix.
- Dave Mark and Kevin Dill,
  [An Introduction to Utility Theory](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter09_An_Introduction_to_Utility_Theory.pdf)
  (Game AI Pro). Response curves; weight on the current action; buckets; deciding when the queue empties.
- Kevin Dill,
  [Dual-Utility Reasoning](https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter03_Dual-Utility_Reasoning.pdf)
  (Game AI Pro 2). Rank, then weight; drop low options; weighted random among the near-best.
- Bill Merrill,
  [Building Utility Decisions into Your Existing Behavior Tree](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter10_Building_Utility_Decisions_into_Your_Existing_Behavior_Tree.pdf)
  (Game AI Pro). A utility selector must expand its child subtrees; cache scores or compute them in a
  separate pass.
- [UnrealUtilityAI](https://github.com/Jay2645/UnrealUtilityAI) (MIT; `DecisionScoreEvaluator.cpp`).
  - The compensation formula and its worked example (25 terms of 0.9 give 0.072, compensated to 0.136).
  - It attributes the formula to Dave Mark's GDC 2015 talk, which was not opened.
  - Its early-out compares an uncompensated partial score. The advice to compare like with like is
    inference from reading that code.
- Damian Isla,
  [Handling Complexity in the Halo 2 AI](https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai)
  (GDC 2005).
  - Defines dithering, and gives the previous winner a bonus against it.
  - Persistence lockouts; behaviour tags as bit vectors.
  - 30 Hz; storage estimates.

## Jobs, claims and priorities

- RimWorld Wiki, [Work](https://rimworldwiki.com/wiki/Work) and
  [Code_MendingJob](https://rimworldwiki.com/wiki/Modding_Tutorials/Code_MendingJob). Community
  sources.
  - All work of one priority is done before the next; ties go left to right.
  - Hauling at the top priority hauls everything.
  - A reservation is taken before the first step, and the job aborts before it begins if that fails.
  - Steps carry fail conditions.
- Oxygen Not Included Wiki, [Priority](https://oxygennotincluded.wiki.gg/wiki/Priority). A community
  source: priority bands, a default sub-priority of 5, and needs that bypass priorities.
- Introversion forums, [job queue description](https://forums.introversion.co.uk/viewtopic.php?t=45058)
  (2013). A community member, not a developer.
  - Jobs are generated by triggers and linked to objects.
  - A valid path assigns the job and moves it to in progress.
- Shining Rock Software, [Laborer update](https://shiningrocksoftware.com/2014-05-31-laborer-update/)
  (2014). Professions stay near home unless a job is fairly old; a player reports distant building
  never happening.
- [HumanResources issue #107](https://github.com/jptrrs/HumanResources/issues/107). Pawns idle while a
  bill is reserved but not worked. The cause is unconfirmed, so it illustrates the symptom, not a proven
  leak.
- The lease on claims, the expiry sweep, the claim indexes and the oldest-job-age check are
  recommendations. No source shows them shipped.

## Cadence, scale and proof

- [Efficient Event-Based Simulations](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter02_Efficient_Event_Based_Simulations.pdf)
  (Game AI Pro Online 2021).
  - A min-heap of timed callbacks.
  - At 60 FPS the frame is 16.7 ms.
  - Time-slicing reduces spikes, does not improve the average frame rate, and can starve.
  - Its printed time-slice listing has bugs.
- [Clanfolk discussion](https://steamcommunity.com/app/1700870/discussions/3/3468352315400813249/)
  (Steam, 2022). Animals die of thirst beside water; the developer replies that the AI slicer cannot keep
  up with the population.
- [Phenomenal AI Level-of-Detail Control with the LOD Trader](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter14_Phenomenal_AI_Level-of-Detail_Control_with_the_LOD_Trader.pdf)
  (Game AI Pro).
  - 57 µs per frame and 48 bytes per entity.
  - No distance threshold can respect a budget.
  - Its printed listing has bugs.
- Unreal Engine,
  [Mass Gameplay overview](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-gameplay-in-unreal-engine?lang=en-US).
  Simulation LOD balances computation load; representation LOD handles visuals.
- Tarn Adams,
  [Simulation Principles from Dwarf Fortress](https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter41_Simulation_Principles_from_Dwarf_Fortress.pdf)
  (Game AI Pro 2). Operate at the level of what the player sees, or one layer below.
- [Automated AI Testing](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter01_Automated_AI_Testing_Simple_tests_will_save_you_time.pdf)
  (Game AI Pro Online 2021). Tests that wait for a condition with a timeout; most bugs reproduce with two
  characters.
- [How to Build Robust AI for Your Game](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter07_How_to_Build_Robust_AI_for_Your_Game.pdf)
  (Game AI Pro 3). Checks for groups reacting in perfect synchrony and for stuck states.
- [Debugging AI with Instant In-Game Scrubbing](https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter06_Debugging_AI_with_Instant_In-Game_Scrubbing.pdf)
  (Game AI Pro 3). A fixed-memory recorder that captures behaviour-tree branches and where execution
  stopped.
- OpenTTD, [desync documentation](https://github.com/OpenTTD/OpenTTD/blob/master/docs/desync.md).
  Sorting with equal keys and stale caches cause desyncs.
- Bettner and Terrano,
  [1500 Archers on a 28.8](https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond)
  (2001). Lockstep needs equal random-call counts and checksums.
- The advice that about four times as many independent runs halves a confidence interval is standard
  sampling arithmetic, stated in the simulation-output literature.

## Not relied on

Decompiled commercial game code is not cited or paraphrased, even where it was consulted to confirm
behaviour. The largest decompilation of one colony sim was removed under a takedown on 2026-10-12, and
the game's licence forbids redistributing decompiled code. Specific cadences and thresholds known only
from decompiled code are left out. The deadband, hashed-phase and thrash-tripwire patterns are stated
without them.

Not opened: Dave Mark's GDC talks on the infinite axis utility system, the AI Arborist talk, Alex
Champandard's articles, and "The Sims Under the Hood". No source gives per-agent decision milliseconds for
a colony sim, or a shipped starvation or livelock detector.

Last checked 2026-10-25.
