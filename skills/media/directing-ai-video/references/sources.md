# Directing AI video source basis

Provider documentation establishes current frame-conditioning controls; research and practitioner
reports establish where chained and interpolated clips fail. Checked 2026-10-27. Durations, models
and controls change; check the selected model's documentation before relying on one.

## Short clips, one motion, image as first frame

- [OpenAI Cookbook — Sora 2 prompting guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide): "The model generally follows instructions more reliably in shorter clips"; stitching two short clips can beat one long one; "Each shot should have one clear camera move and one clear subject action"; the input image is "an anchor for the first frame, while your text prompt defines what happens next"; "The image must match the target video's resolution"; reuse phrasing across shots for continuity.
- [Veo on Vertex AI — Best practices](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice): "For short videos, dedicate each prompt to a single, focused moment"; with an input image, "Focus your prompt on the motion you want to see"; refer to the character plainly ("the subject"); paste the unchanged character description into every prompt.
- [Veo on Vertex AI — Prompt guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide): subject, action, camera motion and composition as separate prompt elements; clear, direct prompts.
- [Runway — Creating with Gen-4](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4): the input image becomes the first frame; clip lengths of a few seconds. Runway's prompting guide could not be fetched (HTTP 403); its advice to describe motion rather than the image and to phrase positively is reported only through third-party summaries and is not relied on alone.

## First and last frame conditioning

- [Veo on Vertex AI — First and last frames](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-first-and-last-frames): a first frame and optional last frame; clip durations of 4, 6 or 8 seconds; 16:9 or 9:16 output.
- [Kling — Start and end frames](https://kling.ai/quickstart/ai-video-start-end-frames): "the content of the first and last frame videos should be as similar as possible"; "significant differences may cause a lens switch". Direct provider evidence for never pinning a distant destination as the end frame.
- [Luma — Video generation API](https://docs.lumalabs.ai/docs/video-generation): start frame, end frame and both, and a `loop` option. The page gives examples without prose on loop behavior; the same-frame-both-ends loop rule is the portable form, usable on any generator with first and last frame inputs.

## Large gaps melt in the middle

- [Generative Inbetweening through Frame-wise Conditions (FCVG)](https://arxiv.org/abs/2412.11755): temporal instability from "the ambiguous interpolation path between two key frames ... becomes particularly severe when there is a large motion gap between input frames".
- [Generative Inbetweening: Adapting Image-to-Video Models for Keyframe Interpolation](https://arxiv.org/abs/2408.15239): distant keyframes are the hard case for coherent in-between motion.
- [Keyframe divide-and-conquer for large motion](https://arxiv.org/abs/2504.08366): splits a large motion into recursively generated intermediate keyframes until each gap is small. Research form of "one human step at a time".
- Together these support judging the middle of a clip, not its endpoints: the endpoints are conditioned and the failure is between them.

## Chains drift

- [InfLVG](https://arxiv.org/abs/2505.17574): autoregressive extension shows progressive quality loss, such as faces growing more saturated. Basis for continuing from accepted frames, re-checking identity against the anchor at every clip, and keeping chains short.
- [How to extend an AI-generated video clip past its length limit without the drift](https://hackernoon.com/how-to-extend-an-ai-generated-video-clip-past-its-length-limit-without-the-drift): practitioner report of colour, light and face drift after a few extensions. Anecdotal.

## Grok Imagine

- [xAI — Video overview](https://docs.x.ai/developers/model-capabilities/video/overview): the model comparison (frame pinning and keyframes only on `grok-imagine-video-1.5`; editing up to 8.7 s and extension of 2–10 s only on `grok-imagine-video`; resolutions; native audio with lip-synced speech); image-to-video output matches the still's aspect ratio; requests are asynchronous.
- [xAI — Video generation](https://docs.x.ai/developers/model-capabilities/video/generation): the image is the starting frame; `duration` 1–15 s, default 8; resolution default 480p; audio on by default with an option for a silent video; returned URLs are temporary.
- [xAI — Reference-to-video](https://docs.x.ai/developers/model-capabilities/video/reference-to-video): `image`, `last_frame` ("pins the exact last frame"), up to four `keyframes` with `timestamp_s` on a third-of-a-second grid; references by position as `<IMAGE_n>`; the same image as `image` and `last_frame` makes a loop; reference clips up to 720p; give each reference one role and keep the cast small.
- [xAI — Video extension](https://docs.x.ai/developers/model-capabilities/video/extension): continues "from the last frame of the input" and returns original plus extension in one file, capped at 720p, on the older model.
- Grok Build 1.0.70's bundled video guidance (shipped with the CLI): the `reference_to_video` tool and its parameters, tag order, tier gating, staging a first frame for multi-element shots, and stating motion as a change of position because bare verbs become bobbing in place. It extracts the last frame with a time seek, which this skill replaces with the exact frame index.
- The advice to prefer chaining over extension, and to generate a sequence at one resolution, is inference from these limits, not xAI guidance.

## Reels and cut grammar

- [OpenAI Cookbook — Sora 2 prompting guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide): describe a shot "as if you were sketching it onto a storyboard"; "keep each shot block distinct: one camera setup, one subject action, and one lighting recipe"; "keeping lighting logic consistent is what makes the edit seamless"; naming three to five colours keeps the palette stable across shots.
- [MasterClass — Continuity editing](https://www.masterclass.com/articles/continuity-editing-in-film-explained) and [Epidemic Sound — Continuity editing techniques](https://www.epidemicsound.com/blog/what-is-continuity-editing/): match on action, eyeline match, the 180-degree rule and the 30-degree rule as the standard techniques that make cuts read as continuous.
- [Filmdaft — The 30-degree rule](https://filmdaft.com/what-is-the-30-degree-rule-in-film/): a camera change under about 30 degrees between shots of the same subject reads as a jump cut.
- [StudioBinder — Walter Murch's Rule of Six](https://www.studiobinder.com/blog/walter-murch-rule-of-six/): emotion, story, rhythm, eye-trace, the two-dimensional screen plane and three-dimensional space, in priority order, from Murch's *In the Blink of an Eye*. Basis for "emotion and story outrank geometry" and for matching the eye across a cut. Secondary summaries; the book itself was not read.
- Trimming generated clips to the action (static starts, drifting ends) is owner practice.

## Frame extraction and assembly

- [ffmpeg documentation](https://ffmpeg.org/ffmpeg.html): an input `-ss` seeks "to the closest seek point before position"; `-sseof` seeks relative to the end; `-frames:v` stops after a frame count; `-vn/-an/-sn/-dn` skip video, audio, subtitle and data streams; `-fps_mode cfr` duplicates and drops frames to an exact constant rate, `passthrough` keeps each frame's timestamp.
- [ffprobe documentation](https://ffmpeg.org/ffprobe.html): `-count_frames` counts frames per stream by decoding.
- [ffmpeg filters — timeline editing](https://ffmpeg.org/ffmpeg-filters.html): `n` is the "sequential number of the input frame, starting from 0", so the last frame is N−1.
- The commands in [frames and assembly](frames-and-assembly.md) were run on ffmpeg 8.1 against a synthetic 72-frame clip: the frame count, the N−1 select, the stream strip, the trim and the concat frame total (72 + 71 = 143) behaved as written.

## Owner practice, not externally sourced

From the catalog owner's production experience directing continuous character footage. No public
source states these; they are the first rules to re-test when models change.

- Subtle by default: movements and expressions sized small unless the brief asks for more, and
  small human expressions (blinks, breaths, a forming smile) rather than theatrical ones.
- A hold line or do-not line in every prompt, plus the provider's negative-prompt field where one
  exists, naming categories of change (nothing appears or disappears, clothing and light unchanged).
  This supersedes an earlier positive-only rule; the caveat that a vivid noun can plant itself on
  models without a negative channel rests on [Black Forest Labs — Negative prompting](https://docs.bfl.ai/guides/prompting_guide_t2i_negative).
  Veo and Kling document negative-prompt inputs.

- Entry, loop and exit clips sharing one rest frame.
- Changing place one human step at a time, as the practical form of the inbetweening research above.
- Judging about one frame per second, and treating similarity scores as a filter, never acceptance.
- Keeping visible life (breathing, weight shift) in every clip.
- Generating new versus editing: describe light and camera only for an image with no parent; in an
  edit, hold light, colour, camera and background by reference to the image and never re-describe
  them, because a description is re-rendered and the light shifts. Consistent with Black Forest
  Labs' "Change nothing else" examples and the Gemini "Do not change any other elements" example.
- Directing natural human movement: stating the pace (generators drift toward slow motion), feet
  planted while weighted, motion in its causal order, small turns because identity drifts through
  profile, hands and feet kept in frame. Consistent with the inbetweening research on large motion
  and the Sora guide's one-action rule; not stated by any provider.
- No crossfades between clips; hard cuts on a shared frame.
- Staging candidates outside shipped media and installing only complete chains.
- Continuing a passing entry from its real last frame rather than refilming it; a run that installs
  nothing has failed.
- The shot brief, take log with rejection reasons, and near-duplicate check.
