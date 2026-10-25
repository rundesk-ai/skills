# Game pathfinding source map

Use this file to audit a rule, not as more procedure. Every source below was opened on 2026-10-25.
Pseudocode in this skill is written fresh from the algorithms the sources describe. No code is copied
from them, and licensed source trees were read only for their behaviour.

## Workload, search space and the A* implementation

- Steve Rabin and Nathan Sturtevant,
  [Pathfinding Architecture Optimizations](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter17_Pathfinding_Architecture_Optimizations.pdf)
  (Game AI Pro, 2013).
  - Measured a roughly 100× spread between A* implementations of one assignment (about 200 µs to
    over 20,000 µs).
  - Allocation during search costs at least an order of magnitude.
  - Search time is proportional to nodes searched; the same area takes 65 grid nodes against a handful
    of waypoint or navmesh nodes.
  - Recommends a per-search id instead of resetting node flags; breaking equal-f ties toward larger g;
    weights of 1.1–1.5, lowered when paths must double back; unordered open lists below about 10–30
    nodes; bucket queues; not stepping back to the parent.
  - Rejects whole-path caching, bidirectional A*, and time-slicing many simultaneous searches, and
    proposes the two-lane short/long queue.
  - Its figures come from student contests on grid maps, not from a shipped title.
- Amit Patel, [Heuristics](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) and
  [Implementation notes](http://theory.stanford.edu/~amitp/GameProgramming/ImplementationNotes.html).
  Both were read from a 2024 web archive snapshot, because the live host refused connections.
  - The heuristic must be in the units of the cost function.
  - Gives the Manhattan, diagonal and octile formulas, and warns against squared Euclidean distance.
  - Gives the tie-breaking options and differential (landmark) heuristics.
  - Recommends a binary heap as the default open set, with bucket queues as an alternative.
- Red Blob Games, [Implementation of A*](https://www.redblobgames.com/pathfinding/a-star/implementation.html)
  and [Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html).
  - Push duplicates rather than decrease-key.
  - Skipping on "visited" instead of comparing cost misses shortest paths.
  - Exit when the goal is popped.
  - Troubleshoot an overestimating heuristic by setting it to zero.
- OpenTTD YAPF source ([yapf_base.hpp](https://github.com/OpenTTD/OpenTTD/blob/master/src/pathfinder/yapf/yapf_base.hpp),
  [nodelist.hpp](https://github.com/OpenTTD/OpenTTD/blob/master/src/pathfinder/yapf/nodelist.hpp),
  [pathfinding_settings.ini](https://github.com/OpenTTD/OpenTTD/blob/master/src/table/settings/pathfinding_settings.ini)).
  - The search stops at a node limit (default 10,000, range 500–1,000,000) and returns the best visited
    node.
  - It keeps an open hash beside a binary heap, and logs a cache-hit ratio.
  - It asserts when a closed node is later reached more cheaply, blaming an estimate that is too large
    or a cost that is too small.
  - GPLv2: studied, not copied.
- Moving AI Lab, [grid benchmarks](https://www.movingai.com/benchmarks/grids.html) and
  [formats](https://www.movingai.com/benchmarks/formats.html). Maps from shipped games, with scenario
  files listing optimal lengths; the lengths assume √2 diagonals and no corner cutting.

## Reachability and regions

- Ludeon Studios, [Reachability at last](https://ludeon.com/blog/2013/07/reachability-at-last/)
  (2013; read from an archive snapshot).
  - A* toward an unreachable target searches the entire map and made a frame take ten times longer.
  - Fixed with flood-filled zone labels: about 5.5 ms for a full rebuild on a 200×200 map, too slow per
    frame; local regeneration was planned.
  - This is an early-development account, not current RimWorld code.
- [How Dwarf Fortress is built](https://stackoverflow.blog/2021/07/28/700000-lines-of-code-20-years-and-one-developer-how-dwarf-fortress-is-built/)
  (Stack Overflow blog, 2021).
  - Its developer says connected components cut almost all failed A* calls.
  - Jump point search and larger precomputed structures are unusable on a map that changes so much.
- Dwarf Fortress Wiki, [Path](https://dwarffortresswiki.org/index.php/DF2014:Path). A community
  source, describing DF2014:
  - in edge cases A* searches every tile;
  - inaccessible items are treated as forbidden for a time;
  - one-wide corridors raise the pathfinding burden.
- Shining Rock Software,
  [Tech stuff 3: pathfinding](https://shiningrocksoftware.com/2013-04-29-tech-stuff-3-pathfinding/)
  (2013).
  - A flood-fill accessibility map is re-run when buildings or bridges change.
  - Walkers keep checking accessibility and repath or cancel.
  - About a 20× speedup over the first A*, and about 350 lines of C++ in all.
- OpenTTD water regions ([water_regions.cpp](https://github.com/OpenTTD/OpenTTD/blob/master/src/pathfinder/water_regions.cpp)):
  - labels local to fixed square regions, with a valid flag;
  - lazy recomputation on read;
  - invalidation of the neighbouring region when an edge tile changes.
  GPLv2: studied, not copied.

## Hierarchy, jump points and precomputation

- Botea, Müller and Schaeffer,
  [Near Optimal Hierarchical Path-Finding](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=b0f0432ba69e4d730b93a75e3d19c8e9d811efac)
  (2004).
  - HPA* clusters with entrance transitions, and lazy refinement.
  - Inserting start and goal comes to dominate cost as levels are added.
  - Up to 10× faster than optimised A*, within 1% of optimal after smoothing.
  - On 2004 hardware.
- Harabor and Grastien,
  [Online Graph Pruning for Pathfinding on Grid Maps](https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf)
  (AAAI 2011). Jump point search: optimal on uniform-cost grids, needs no preprocessing or memory, and
  gives a speedup of an order of magnitude and more.
- Rabin and Silva,
  [JPS+](https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter14_JPS_Plus_An_Extreme_A_Star_Speed_Optimization_for_Static_Uniform_Cost_Grids.pdf)
  (Game AI Pro 2). Requires a static map; up to 100× over A*; uses a bucket open list.
- Rabin and Sturtevant,
  [Faster A* with Goal Bounding](http://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter22_Faster_A_Star_with_Goal_Bounding.pdf)
  (Game AI Pro 3). About 8× on grids; changing a single node, edge or cost invalidates all the
  precomputed data.
- Sturtevant and Rabin,
  [Faster Dijkstra Search on Uniform Cost Grids](http://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter23_Faster_Dijkstra_Search_on_Uniform_Cost_Grids.pdf)
  (Game AI Pro 3). Canonical Dijkstra is 2.5× faster on random maps and 4× on StarCraft maps; jump
  point search overhead grows in open areas.
- Geisberger,
  [Contraction Hierarchies](https://ae.iti.kit.edu/download/diploma_thesis_geisberger.pdf) (2008).
  Nodes are contracted with shortcut edges and queried by an upward bidirectional search; it is static
  preprocessing for road networks.
- Factorio, [Friday Facts 317](https://factorio.com/blog/post/fff-317) (2019). The enemy pathfinder
  keeps an abstract graph of chunk components that ignores entities and is updated only on tile
  changes. That supports choosing an abstraction that frequent edits do not touch.

## Flow fields

- Elijah Emerson,
  [Crowd Pathfinding and Steering Using Flow Field Tiles](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter23_Crowd_Pathfinding_and_Steering_Using_Flow_Field_Tiles.pdf)
  (Game AI Pro; Supreme Commander 2).
  - 10×10 sectors; clear sectors share one cost field; the field bit layouts.
  - A merging A* over portals, flow tiles cached per portal window, a line-of-sight pass, and island
    ids.
  - A wavefront must stop at cells already integrated unless the difference is significant.
  - Dynamic edits run through a priority queue sliced in milliseconds. The skill replaces milliseconds
    with iterations for deterministic simulations; that substitution is inference, not the source's
    advice.
- Red Blob Games, [Flow field pathfinding for tower defense](https://www.redblobgames.com/pathfinding/tower-defense/).
  A flow field is the negative gradient of the distance field; several goals are seeded together.

## Scheduling, budgets and threads

- [recastnavigation](https://github.com/recastnavigation/recastnavigation) (zlib licence), Detour and
  DetourCrowd source:
  - the sliced query API, with partial results to the closest node;
  - a path queue of 8 slots that frees uncollected results;
  - crowd defaults of 100 iterations per update and 4,096 nodes;
  - a 20-iteration quick search, oldest-first replanning, a 10-polygon validity lookahead, a 1 s replan
    delay, and topology optimisation at most every 0.5 s;
  - node-pool clearing by resetting only hash heads.
  Detour uses floats and is not deterministic as shipped.
- SomaSim,
  [Project Highrise architect's notes](https://somasim.com/blog/2016/06/30/project-highrise-architects-notes-for-june-30-2106/)
  (2016). A 15,000-node grid reduced to about 100 nodes and 400 edges, with a job queue and limiter,
  holding 60 FPS.
- Klei, [Oxygen Not Included update notes](https://kleiforums.com/game-updates/oni-alpha/702808-r2638/):
  - fixes to asynchronous path probing for race conditions;
  - unreachable tiles computed as reachable;
  - a pathfinding thread that crashed silently, after which agents could reach only previously
    reachable areas.
  The game is closed source, so these are symptoms only.
- Bettner and Terrano,
  [1500 Archers on a 28.8](https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond)
  (2001). AI pathing made turn times fluctuate by up to 200 ms, and pathfinding was among the systems
  checksummed for lockstep.

The rules on iteration budgets, fixed-tick delivery, request-id ordering and stale-revision discard
are conclusions drawn from these failures. No single source prescribes this exact queue.

## Following, avoidance and groups

- Mikko Mononen,
  [Simple Stupid Funnel Algorithm](http://digestingduck.blogspot.com/2010/03/simple-stupid-funnel-algorithm.html)
  (2010).
  - The portal-based funnel with apex restart.
  - Erode the mesh rather than handle radius in the funnel (about 100× more complicated otherwise).
  - Winding decides left and right, and a bad corridor causes a horizon effect.
  - Readers reported edge cases in the comments.
- van den Berg, Guy, Lin and Manocha,
  [Reciprocal n-Body Collision Avoidance](https://gamma.cs.unc.edu/ORCA/publications/ORCA.pdf).
  - ORCA's linear program becomes infeasible when agents are packed densely.
  - A zero optimisation velocity can deadlock.
  - 5,000 agents in 8–16 ms on 8 cores.
- Craig Reynolds, [Steering Behaviors For Autonomous Characters](http://www.red3d.com/cwr/steer/gdc99/)
  (GDC 1999). Path following by predicting and correcting onto the path spine; separation; combining
  behaviours.
- Mars and Chanut,
  [Hierarchical Architecture for Group Navigation Behaviors](https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter20_Hierarchical_Architecture_for_Group_Navigation_Behaviors.pdf)
  (Game AI Pro 2). A virtual group entity with member steering. Avoiding obstacles with the whole
  group as one disc is very conservative, and exact slot assignment is factorial, so it is approximated
  greedily.
- Koenig and Likhachev, [D* Lite](http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf) (AAAI 2002).
  Designed for repeated replanning by a robot moving through unknown terrain, searching from the goal.
  The skill's advice to prefer labels and requeued searches for crowds is inference from that design
  case, not a measured comparison.

## Not relied on

Decompiled commercial game code is not cited: a decompilation mirror of one colony sim was removed
under a takedown in 2026, and its licence forbids redistribution. The Planetary Annihilation, Age of
Empires IV and Cities: Skylines pathfinding internals were not opened. No source gave a shipped stuck
timer, per-tick request budgets for those titles, or measured hit rates for merged duplicate requests.
The merge pattern is therefore inference from the queues above.

Last checked 2026-10-25, against the live pages or the archive snapshots named above.
