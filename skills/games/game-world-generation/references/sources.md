# Sources

This skill synthesizes procedural-content-generation
research and procedural urban-modeling papers. It is not a systematic
review and does not prescribe one algorithm, noise function, city grammar, seed count, metric set,
or visual style. The correct representation and evaluation depend on the generated content, the
game's rules, the production context, and the intended players.

## Scope, generator choice, and controllability

- Shaker, Togelius, and Nelson,
  [*Procedural Content Generation in Games*](https://www.pcgbook.com/)
  (Springer, 2016; DOI `10.1007/978-3-319-42716-4`), provides the field definition and chapters on
  search, constructive generation, noise and agents, grammars, rules, planning, mixed initiative,
  experience-driven generation, and evaluation. Chapter 1 distinguishes online/offline,
  necessary/optional, controlled/uncontrolled, deterministic/stochastic, constructive/generate-and-
  test, and automatic/mixed-authorship uses. It also identifies speed, reliability, controllability,
  expressivity, diversity, creativity, and believability as potentially competing properties. This
  supports defining purpose and tradeoffs before choosing a method; the 2016 text is a field overview,
  not a current guarantee that any listed technique meets a production game's needs.
- Shaker et al.,
  [Chapter 3: “Constructive Generation Methods for Dungeons and Levels”](https://www.pcgbook.com/chapter03.pdf),
  describes controllability as a designer's ability to steer generation while preserving intended
  properties and variability, then surveys partitioning, agent-based, cellular-automata, grammar,
  and platform-level methods. This supports matching a representation to its desired control surface,
  not treating any family as universally superior.
- Liapis, Smith, and Shaker,
  [Chapter 11: “Mixed-Initiative Content Creation”](https://www.pcgbook.com/chapter11.pdf),
  treats human and computational creators as sharing initiative; discusses direct and indirect
  control, constraint conflicts, human authority, target audience, and generator explanation. It
  supports protected edits, conflict reporting, reviewable proposals, and semantic regeneration.
  The examples are research tools and do not establish one production editor workflow.

## Staged causal world construction

- Parish and Müller,
  [“Procedural Modeling of Cities”](https://people.eecs.berkeley.edu/~sequin/CS285/PAPERS/Parish_Muller01.pdf)
  (SIGGRAPH 2001), presents a pipeline from geographical and sociostatistical input maps to roads,
  blocks, lots, buildings, and visualization. Its road system combines global goals with local
  constraints, while later stages depend on earlier semantic products. This supports broad-to-detail
  staged generation, causal inputs, and local/global validation. Its L-system, assumptions, visual
  goals, and reported hardware timings are historical and are not generalized as current game-world
  requirements.
- Chen et al.,
  [“Interactive Procedural Street Modeling”](https://peterwonka.net/Publications/pdfs/2008.SG.Chen.InteractiveProceduralStreetModeling.pdf)
  (ACM Transactions on Graphics 27(3), 2008; DOI `10.1145/1360612.1360702`), presents interactive
  creation and modification of
  large street networks. It is supporting evidence that city generation can expose controllable,
  editable intermediate network structure rather than emit only final geometry. It addresses street
  modeling and visual urban geometry, not a complete playable-world or runtime-simulation contract.

## Validation and distribution evidence

- Shaker, Smith, and Yannakakis,
  [Chapter 12: “Evaluating Content Generators”](https://www.pcgbook.com/chapter12.pdf),
  distinguishes top-down content-statistic analysis from bottom-up player evaluation, recommends
  representative samples when studying expressive range, and argues that a hybrid can better reveal
  what a generator does and whether it fits its intended job. This supports seed suites,
  distribution-aware metrics, and player inspection. The chapter does not supply one sufficient
  metric set or universal sample size.
- Summerville,
  [“Expanding Expressive Range: Evaluation Methodologies for Procedural Content Generation”](https://ojs.aaai.org/index.php/AIIDE/article/view/13012)
  (AIIDE 2018; DOI `10.1609/aiide.v14i1.13012`), notes the lack of a commonly accepted PCG assessment
  methodology and proposes techniques intended to expose strengths and weaknesses while reducing
  ad-hoc, cherry-picking-prone evaluation. It supports showing distributions, comparisons, and
  unusual cases instead of a favorite seed. The methods were demonstrated on particular generator
  representations and do not make arbitrary metric pairs meaningful.

## Reproducibility, boundaries, and synthesized conclusions

- The PCG book distinguishes seeds, parameter control, and deterministic from stochastic generation;
  it notes that a seed can reproduce content when the generating method is held constant. The skill's
  broader identity record—generator version, normalized configuration, inputs, overrides, stream
  policy, and compatibility envelope—is a conservative reproducibility conclusion because a seed
  alone does not freeze those other dependencies.
- The staged pipeline combines the PCG taxonomy with Parish and Müller's explicit road-to-lot-to-
  building dependencies. The exact substrate, field, biome, network, parcel, and population stages
  are optional semantic categories, not a copied universal pipeline.
- The independent-stream rule applies the reproducibility objective to editable staged generation.
  No cited source requires a particular random-number generator or derivation function.
- Hard invariants, soft objectives, and distribution targets synthesize the PCG book's reliability,
  controllability, expressivity, generate-and-test, and evaluation distinctions. The bounded repair
  ladder and structured failure records are production-safety conclusions, not a published taxonomy.
- The disconnected-site good/bad pair applies the book's requirement that necessary content be
  correct and the evaluation sources' warning against cherry-picking. The exact repair is intentionally
  conditional on the game's route contract.
- Provenance guidance is a conservative boundary, not legal advice. The skill requires recorded
  origin, version, terms, transformation, and approval because generator inputs and output rights vary;
  a qualified owner must decide whether a dataset, model, template, asset, or output may be used or
  distributed.
