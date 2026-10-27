# Directing character images source basis

Provider documentation establishes what current models offer for reference-conditioned editing;
it is evidence for the portable rule, not syntax to copy. Checked 2026-10-27. Model names and
controls change; check the selected model's current documentation before relying on one.

## Edit an accepted image rather than regenerate

- [Gemini API — Image generation](https://ai.google.dev/gemini-api/docs/image-generation): "Multi-turn conversation is the recommended way to iterate on images"; models accept several character reference images "to maintain character consistency"; one lighter model is documented as not optimized for multi-turn sequential editing, so the capability is model-specific.
- [Introducing Gemini 2.5 Flash Image](https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/): names keeping a character or object the same across prompts and edits as a fundamental challenge of image generation.
- [FLUX.1 Kontext paper](https://arxiv.org/abs/2506.15742) and [announcement](https://bfl.ai/blog/flux-1-kontext): an editing model trained for successive edits, evaluated for drift across chained edits and for identity preservation across scenes. Supports editing from an accepted image as the consistency mechanism.
- [OpenAI Cookbook — Generate images with high input fidelity](https://developers.openai.com/cookbook/examples/generate_images_with_high_input_fidelity): with high input fidelity "faces are preserved far more accurately"; "Use this when you need people to remain recognizable across edits"; the first input image keeps the finest detail, so the identity reference goes first; multiple faces are best combined into one composite input.
- [Veo on Vertex AI — Best practices](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice): "Your character description is the foundation for consistency" and "Copy and paste the entire, unchanged character description" into every prompt. Basis for reusing the written anchor description verbatim.
- [Midjourney — Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds): seeds are not reliable across sessions or changed settings and are weaker than references. Basis for preserving accepted images rather than seeds.

## One change per edit and the edit grammar

- [OpenAI Cookbook — Sora 2 prompting guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide): make "controlled changes – one at a time – and say what you're changing"; keep a close result as the reference and describe only the adjustment; reuse phrasing for continuity and "avoid mixing traits that may compete".
- [Black Forest Labs — Single-reference editing](https://docs.bfl.ml/guides/prompting_editing_single_reference.md): examples name what must stay ("Preserve its identity, head position, feather pattern, pose, lighting and the rest of the scene", "Change nothing else"). Basis for stating what stays, by name.
- [Black Forest Labs — Image editing overview](https://docs.bfl.ml/guides/prompting_editing_overview.md): give each input image a role and refer to it by position; output aspect ratio follows the first image unless set. Basis for one job per reference and for matching the target aspect ratio.
- [Black Forest Labs — Negative prompting](https://docs.bfl.ai/guides/prompting_guide_t2i_negative) and [Imagen negative prompts](https://cloud.google.com/vertex-ai/generative-ai/docs/image/omit-content-using-a-negative-prompt): models without a negative channel; positive desired states recommended; negative fields limited to named models.

## Whole-frame inspection

- [HandRefiner](https://arxiv.org/abs/2311.17957): diffusion models "suffer from generating accurate human hands, such as incorrect finger counts or irregular shapes". Basis for inspecting hands and limbs, not only the face.
- [T2I-CompBench](https://arxiv.org/abs/2307.06350) and [TIFA](https://arxiv.org/abs/2303.11897): attribute binding, counting and spatial relations fail measurably. Basis for checking garments, props, counts and placement against the anchor.

## Prompting for a realistic person and Grok Imagine

- [xAI — Imagine overview](https://docs.x.ai/developers/model-capabilities/imagine): `grok-imagine-image-2.0` for image generation and editing.
- Grok Build 1.0.70's bundled image guidance (shipped with the CLI, not published as a web page): `image_gen` and `image_edit`, references downscaled to about 768 pixels on the long side, single-image edits keep the input aspect ratio, no count parameter, prompt order subject → action → setting → style → composition → lighting, positive description, two to five sentences, reference-first for real people.
- [Veo on Vertex AI — Prompt guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide) and [Google Cloud — Imagen prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide): camera position, lens and lighting as concrete prompt elements that change output.
- That "perfect" or "flawless" skin wording produces a smoothed, plastic face is owner practice, not sourced.

## Owner practice, not externally sourced

These rules come from the catalog owner's production experience directing a recurring character.
No public source states them; they are kept because each prevents a failure the owner observed, and
they are the first candidates to re-test when models change.

- Subtle by default: movements and expressions sized small unless the brief asks for more, and
  small human expressions (blinks, breaths, a forming smile) rather than theatrical ones.
- A hold line or do-not line in every prompt, plus the provider's negative-prompt field where one
  exists, naming categories of change (nothing appears or disappears, clothing and light unchanged).
  This supersedes an earlier positive-only rule; the caveat that a vivid noun can plant itself on
  models without a negative channel rests on [Black Forest Labs — Negative prompting](https://docs.bfl.ai/guides/prompting_guide_t2i_negative).
  Veo and Kling document negative-prompt inputs.

- Naming a feature to protect it exaggerates it over successive edits. Consistent with the Sora
  guide's warning against competing traits, but not stated by any provider.
- Two misses on the same edit mean change the input image, not the wording.
- A near-duplicate check against existing accepted images before generating.
- Keeping rejected candidates out of delivery, with the rejection reason.
- The top-to-bottom body inspection beyond hands (proportions, feet and toes, posture a body could
  hold) and naming the support for a leaning or sitting pose. HandRefiner establishes the hand
  failure; the same check is extended to the rest of the body from observed failures.
- A reference set of angles made from the anchor by edits.
- Generating new versus editing: describe light and camera only for an image with no parent; in an
  edit, hold light, colour, camera and background by reference to the image and never re-describe
  them, because a description is re-rendered and the light shifts. Consistent with Black Forest
  Labs' "Change nothing else" examples and the Gemini "Do not change any other elements" example.

## Rights

- [U.S. Copyright Office — AI report summary](https://www.copyright.gov/newsnet/2025/1060.html): prompts alone do not establish authorship; human selection and modification may. Provider policies on real people and public figures vary and are checked per provider.
