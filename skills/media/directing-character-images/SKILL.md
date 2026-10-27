---
name: directing-character-images
description: Use when generating or editing AI images of a recurring character, above all a realistic person, who must keep the same face and a believable body across images, including new poses, outfits, expressions, scenes or angles from a reference picture, fixing a character who drifted or came out wrong, asking why edits keep failing, or making a character's keyframes for a video generator. It supplies a provider-neutral edit-first workflow for identity lock, one change per edit, prompt grammar with worked examples, whole-body inspection, and how to diagnose and improve a failed take. Do not use it for logos, icons, illustrations or textures, game sprites, or one-off images with no recurring character.
---

# Directing character images

A character stays the same only when every new image descends from an image already accepted.
Text alone describes a category, not a person: two prompts with identical words give two different
faces. So the default is to **edit an accepted image**, never to regenerate the character from text.

## Lock the identity first

1. Collect the reference: one sharp, evenly lit image of the character, face and full body visible,
   at the highest resolution available. Everything later descends from it, so a blurry or stylized
   reference bakes its defects into every image.
2. Make the anchor from it: the character in a neutral standing pose, plain background, the outfit
   and props the work needs. Inspect it (below) before anything is built on it.
3. Write the identity card: build, height, age, face shape, hair, skin, outfit piece by piece,
   props and which hand or shoulder carries each. Reuse it word for word in every prompt; changed
   wording invites changed traits.
4. When the work needs other angles, make a small reference set from the anchor by edits: three-
   quarter, profile, back. Later edits that turn the character use the matching angle as reference
   instead of asking the model to invent the unseen side.

## Generating new: write it like a photograph

Only an image with no parent is generated from a description: the first anchor of an invented
person, or a new setting the person has never been in. Once an image exists, every later image is
an edit of it, and the editing rules below replace these.

A realistic person comes from a prompt that describes a photograph, not a rendering. Describe in
this order: the person, what they are doing, the setting, then the camera and the light, in two to
five plain sentences.

```text
Good: The woman from the reference photo stands on a quiet city pavement in the early morning,
holding a paper coffee cup in her right hand. Shot at eye level from about three metres with a
50 mm lens, waist up, background softly out of focus. Soft overcast daylight from the left, natural
skin texture, true-to-life colour.

Bad: Ultra-realistic 8K masterpiece, stunning beautiful woman, perfect flawless skin, cinematic
lighting, trending, highly detailed.
```

- **Name a real light source and its direction** (window light from the left, overcast sky, a desk
  lamp behind her). "Cinematic lighting" lets the model invent one per image, and the person's face
  changes shape with it.
- **Name the camera**: height, distance, lens, framing. A fixed camera recipe across a set keeps
  proportions comparable from image to image.
- **Ask for natural skin and texture**, never "perfect" or "flawless": those words give the smooth
  plastic face that reads as generated, and the smoothing erases the identity.
- **One scene per prompt, one person unless the shot needs more.** Every extra person splits the
  identity budget, and faces start to blend.
- **Real people need a real reference.** Never generate a named real person from text; edit a
  photo the project has the right to use.

When the tool has an identity or input-fidelity control, or accepts several reference images, use
it and put the identity reference first; providers that weight inputs unevenly weight the first.
Give every reference one job ("image 1: the character; image 2: the jacket only").

## Editing: hold what exists, describe only the change

Editing is the opposite of generating. The image already has its light, camera, colour and setting;
the prompt's job is to leave them alone. Every word of description is an instruction the model
re-renders to its own reading, so an accurate description of the existing light still shifts its
direction, colour or contrast. Describe only the one change, and hold everything else by reference
to the image.

Each new image is an edit of the closest accepted image, changing **one** thing: the pose, or the
outfit, or the setting, or the expression, or the light. Two changes in one edit make a miss
undiagnosable, and the model trades identity for the larger change. A new scene and a new pose is
two edits, with an inspection between them.

Write every edit in three parts: what stays, the one change, everything else unchanged.

```text
Keep: the same woman, same face and hair, same build, grey wool coat buttoned to the collar,
brown leather satchel on her left shoulder.
Change: she sits on the park bench, both hands resting on the satchel in her lap.
Keep the lighting, colour, camera angle, framing and background exactly as they are in the image.
Do not add, remove or move anything else, and do not change her clothes, hair or expression.
```

```text
Bad: Make her sit down on a bench in a nicer park, more cinematic, keep her looking the same,
no extra fingers, keep her freckles.
```

The bad prompt asks for three changes (pose, setting, style), protects identity with a vague
phrase, names defects instead of the wanted state, and names a trait that will be exaggerated.

- **Say what stays before what changes.** Name the person's parts that drift (face, hair, build,
  each garment and prop) briefly and plainly; unnamed parts are what change.
- **Hold the light by reference, never by description.** Write "keep the lighting exactly as it is
  in the image", not "soft daylight from the left". The same holds for camera, framing, colour and
  background. Describe the light only when the light is the one change.
- **Make the change physical and concrete**: where each hand is, which way the head turns, what the
  body rests on. "She relaxes" leaves the model to choose, and it chooses differently each time.
- **Describe the change as the wanted state** ("both hands resting in her lap"), not as a defect to
  avoid ("no extra fingers").
- **End with a do-not line** that holds the rest of the image: nothing added, removed or moved; the
  clothes, hair, expression and light unchanged. Put the same list in the tool's negative-prompt
  field when it has one. Name categories of change, not vivid specifics: on a model without a
  negative channel, a vivid noun ("no dog") can plant the thing it names.
- **Expressions small by default.** Give the size: "a slight closed-mouth smile", "eyes softening",
  "a small frown". Big expressions (a wide grin, open-mouth laughter, wide eyes) stretch the face
  away from the anchor and read as performed; use them only when asked, and check the face against
  the anchor after. A small real expression, a relaxed gaze or the beginning of a smile, is what
  makes a person look human rather than a mannequin.
- **Do not name a feature to protect it.** Words about a trait ("prominent nose", "freckles",
  "muscular") push the model to amplify it on every pass. Let the reference carry it. The identity
  card describes traits plainly and once; it never stresses one.
- **Match the target.** Generate at the resolution and aspect ratio of where the image goes, a
  video clip's frame size included; a reframed or upscaled image loses the identity it was edited to
  keep, and a video generator given the wrong size crops or distorts it.
- **Refer to the character plainly** ("the woman", "the chef") rather than by a new descriptive
  phrase each time.

## Inspect the whole person

Judge every candidate at full size against the anchor, side by side, before accepting it. The face
is the part that gets checked and the body is where it fails. Go through the person top to bottom:

- **Face:** same face shape, eye spacing and colour, nose, mouth, ears, hairline, skin tone, age.
  Both eyes look the same way, teeth are a normal row, nothing is smoothed into a different person.
- **Proportions:** head size against the body, neck length, shoulder width, arm length reaching
  mid-thigh, legs of equal length, the same build and height as the anchor beside the same props.
- **Hands:** five fingers on each hand, each with its joints, nails on the right side, thumbs on the
  right side for left and right hands; a hand that holds something wraps around it with contact.
- **Arms, legs and joints:** two of each, attached where they should be, elbows and knees bending
  the way they can, no limb passing through the body, clothing or furniture.
- **Feet:** two feet, pointing plausibly, standing on the ground with weight; bare feet have five
  toes each, shoes are a pair.
- **Posture:** the pose could be held: weight over the feet, a sitting person supported by the
  seat, a leaning person by what they lean on.
- **Outfit and props:** same cut, colour, pattern, buttons, logo side and layers as the anchor; a
  bag on the same shoulder; nothing that appeared or vanished.
- **Light:** the same direction, colour, softness and contrast as the parent image, shadows falling
  the same way. An edit that relit the image is rejected even when the new light looks better: the
  next image and every video frame from it inherit the change.
- **Scene:** camera angle, framing, colour and background as in the parent; perspective and scale
  agree with the setting; no text, watermark or mangled signage crept in.
- **The one change:** it happened, at the size asked for, and nothing else did: nothing appeared,
  vanished or moved.

Reject on any failure, whatever the image's beauty; a defect accepted here is copied into every
image edited from it, and into every frame of a video started from it.

## Improve a miss

Name what failed before changing anything, then make the one move that targets it:

| What failed | Next move |
|---|---|
| The change did not happen | Make it physical and concrete; put it in its own sentence; split a large change into two steps |
| Identity drifted with the change | Edit from the anchor again, identity reference first; make the change smaller |
| Identity drifted slowly over many edits | Stop chaining from the latest image; go back to the anchor or the last image that matched it |
| A trait grew stronger | Remove every word about it; edit from an image where it was right |
| Face is a different person | Edit from the anchor with the identity reference first; change less per edit; keep the face larger in frame |
| Hands, feet or limbs broken | Describe the grip or pose exactly, limb by limb; crop to the region and edit it; use a pose reference; or compose so the hand is hidden |
| Outfit or prop changed | Name it piece by piece in the keep line; add it as a second reference with that one job |
| Expression too big | Give its size ("a slight closed-mouth smile"); edit again from the parent, not from the exaggerated image |
| Lighting or colour changed | Delete every description of light; write "keep the lighting exactly as in the image"; edit again from the parent |
| Something else changed too | List it by name in the keep line; check that the prompt asked for one change only |

**Two misses on the same edit mean change the picture, not the adjectives.** Start from a closer
accepted image, split the change, crop and edit the region, add a reference for the target pose or
garment, or recompose so the difficult part is out of frame. A third rewording of the same request
spends attempts and drifts the identity further.

Read [improving takes](references/improving-takes.md) for each failure with a before and after
prompt, and a worked sequence from anchor to finished image.

## Keep the record

For every accepted image, keep the file, its parent image, the edit prompt, the model and settings,
and what was checked. Keep rejected candidates out of the delivery folder, with the reason each was
rejected; a later session that cannot see why a take failed generates it again. Preserve accepted
images themselves, not seeds or prompts: hosted models change, and the same request later gives
different pixels.

Before generating a new image, check what already exists: an accepted image that is nearly the
picture needed is edited, not duplicated.

## Rights

Use a real person's likeness only with their consent and the right to use the reference, and follow
the provider's policy on real people, minors and public figures. Record where each reference came
from.

Read [Grok Imagine](references/grok-imagine.md) when making the images with xAI's image models.

Read [the source basis](references/sources.md) when changing a rule or checking a provider control.
