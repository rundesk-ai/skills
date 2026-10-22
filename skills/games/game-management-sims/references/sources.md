# Sources

This skill synthesizes game design research, current public
talk descriptions, studio material, interviews, and postmortems. It does not establish a universal
formula for fun, a required city-simulation architecture, or one ideal amount of detail. The studio
accounts describe particular games and are treated as practitioner evidence.

## Experience and system design

- Hunicke, LeBlanc, and Zubek,
  [“MDA: A Formal Approach to Game Design and Game Research”](https://users.cs.northwestern.edu/~hunicke/MDA.pdf)
  (2004), defines mechanics, runtime dynamics, and intended aesthetic responses; emphasizes the
  different designer and player perspectives; and calls for iterative qualitative and quantitative
  analysis. It supports starting from an audience-specific experience and tracing rules through
  behavior to evidence. MDA explicitly is a framework, not a formula for fun.
- Ryan, Rigby, and Przybylski,
  [“The Motivational Pull of Video Games: A Self-Determination Theory Approach”](https://doi.org/10.1007/s11031-006-9051-8)
  (2006), reports four studies linking perceived autonomy and competence with outcomes in the tested
  games, and relatedness in its MMO study. It supports naming multiple experience hypotheses rather
  than optimizing one engagement measure. The studies do not establish that management mechanics
  automatically satisfy those needs or that the MMO survey associations are universally causal.
- Sylvester,
  [“The Simulation Dream”](https://tynansylvester.com/2013/06/the-simulation-dream/)
  (2013), is a named practitioner's account arguing that simulated relationships have value only when
  players can form a useful mental model, and recommending the minimum representation that supports
  the intended stories. It directly supports the fidelity-budget and legibility guidance. Its
  “player model” and “story-richness” vocabulary is a design heuristic, not controlled evidence or a
  requirement that every management game generate stories.
- Sylvester's GDC 2017 session,
  [“RimWorld: Contrarian, Ridiculous, and Impossible Game Design Methods”](https://www.gdcvault.com/play/1024232/-RimWorld-Contrarian-Ridiculous-and),
  describes framing *RimWorld* as a story generator and deliberately omitting conventionally expected
  features. It supports selecting simulation features by the game's particular promise rather than
  genre completeness. The public overview does not expose a comparative method or universal feature
  test.

## Simulation representation and legibility

- Pierre,
  [“We Built This City on Bits 'n Maps”](https://www.gdcvault.com/play/1034401/We-Built-This-City-on)
  (GDC 2024), presents maps, networks and globals, agents, and building-to-building connections as
  four techniques used on *SimCity* and *Cityscapes: Sim Builder*. It supports distinguishing
  representations by the behavior they need to produce; it is practitioner guidance from two city
  simulations, not proof that every management game needs all four.
- Electronic Arts,
  [“Insider's Look at SimCity's New Simulation Engine”](https://www.ea.com/en-ca/news/insiders-look-at-simcity-new-simulation-engine)
  (2012), describes GlassBox in terms of resources, units, maps, agents, and visible economic, water,
  and fire scenarios under the product's “What You See Is What We Sim” framing. It supports connecting
  visible world changes to underlying systems. It is first-party promotional and explanatory
  material, not independent evidence that its representation was optimal.
- Spasov,
  [“Starting From Scratch: Haemimont Games' Tropico 5 postmortem”](https://www.gamedeveloper.com/audio/starting-from-scratch-haemimont-games-i-tropico-5-i-postmortem)
  (2015), reports that removing individually simulated citizens produced a prototype that no longer
  felt like *Tropico*, while other invisible heavy logic was removed. It also reports cross-system
  failures from transportation changes, live sequence-state debugging, and whiteboxed UI and
  buildings. This supports making agent-versus-aggregate fidelity depend on the player promise,
  exposing system state, and testing full loops before art. It is one sequel's retrospective and
  does not prove that individual agents are preferable in other games.

## Constraint loops, crises, and recovery

- Couture's interview with Ogłoziński,
  [“How Against the Storm managed to mix city-building and roguelite play”](https://www.gamedeveloper.com/business/how-against-the-storm-managed-to-mix-city-building-and-roguelite-play)
  (2023), reports the team's “city is your avatar” framing, pressure against a solved stable state,
  three scoped victory routes, and an exploration route intended to keep a resource-starved run from
  remaining stuck. It supports defining the managed subject, designing multiple bounded routes, and
  preserving a costly escape from limbo. Those choices fit one run-based city-builder and are not a
  prescription to reset every management game or always provide a comeback.

## Good/bad mapping and synthesized conclusions

- The individual-worker pair combines the *Tropico 5* agent-prototype result with Sylvester's minimum-
  representation heuristic. The exact worker example is a portable design test, not a reported
  product result.
- The drought pair applies MDA's mechanics-to-dynamics trace and the *Against the Storm* account of
  pressure, multiple routes, and recovery. No source claims drought is the correct crisis or supplies
  a universal warning window.
- The binding-constraint loop, three nested horizons, four-part explanation view, and automation
  classification are a conservative synthesis. They operationalize MDA, the simulation
  legibility sources, and the cited management-game postmortems; they are not copied taxonomies.
- Autonomy, competence, curiosity, attachment, tension, recovery, and expression are hypotheses to
  select for a named audience. The motivation research supports only a subset directly, so the skill
  requires playtest evidence instead of presenting the list as a validated scale.
