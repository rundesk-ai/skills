---
name: directing-ai-video
description: Use when planning or directing an AI video generator to produce footage of a recurring person or character with a consistent face and natural, believable movement, including one continuous shot or loop built from several short clips, a short reel or sequence of shots with natural cuts, image-to-video, first and last frame clips, entrances, idle loops and exits, extending a clip, or fixing clips that jump, morph, flicker or freeze. It supplies a director's workflow with a plan and shot list before generating, clip chains on real extracted frames, cut grammar, prompts, mid-clip judging, a take log and QC. Do not use it for trimming, colour-matching or cutting together camera footage when no generator is involved, or for in-game sprite animation.
---

# Directing AI video

The agent here is the director. A video generator follows a short instruction for a few seconds
and drifts beyond that; it cannot plan a scene, keep a face across shots or decide where to cut.
Those are the director's job, done on paper before the first generation, then enforced take by take.
The deliverable is finished footage installed where it is used; a run that ends with nothing
installed has failed, however many good takes it produced.

## The workflow at a glance

1. Anchor: an accepted still of the person, at the delivery size and aspect ratio.
2. Plan: choose the form, write the shot list and a brief for every shot, show it to the owner.
3. Keyframes: edit each start frame from the anchor or the last accepted frame, one change each.
4. Generate one clip from its start frame, with a motion-only prompt.
5. Judge it through the middle, not only the ends; log the take and its reason.
6. On a miss, name the failure and change one thing; after two misses, change the frames or plan.
7. On a pass, keep it and build on it: extract its exact last frame for the next continuous clip.
8. Assemble: normalize, hard cuts, no crossfades; play every join or cut.
9. Install the complete sequence, play it where it is used, run the QC list.

## Plan before generating

1. **Choose the form.** A **continuous shot** is one unbroken view: an entrance, a hold, a loop, an
   exit, joined so no cut is visible. A **reel** is a sequence of shots joined by cuts that feel
   natural: different angles and sizes telling one short story. The form decides how clips connect:
   a continuous shot joins on identical frames, a reel joins on matched action and direction.
2. **Read the workflow for that form** before writing a shot:
   [continuous chain](references/continuous-chain.md) or [reel](references/reel.md).
3. **Write the plan**: purpose and length, the shot list, and a brief for every shot (below). When
   someone owns the footage, show them the plan before spending generations; changing a line costs
   nothing, changing a generated chain costs every take after it.
4. **Check what already exists.** A clip that already covers a shot, or nearly does, is reused or
   continued, not generated again.

## Write the shot brief

```text
Shot:       entry-02, the courier walks from the door to the counter
Stays:      the courier (anchor still), uniform, parcel in right hand; shop interior; light
Moves:      the courier, three unhurried steps forward; breathing and parcel sway
Camera:     locked, eye level, medium-wide
Start:      last frame of entry-01, extracted
End:        free (or: keyframe K3, courier at the counter)
Acceptance: same face and uniform throughout, parcel never changes hand, no object appears,
            feet plant and do not slide, joins invisibly to entry-01 and loop-01
```

## Make keyframes by editing, not generating

Every start, end or pinned frame descends from an accepted still of the person. Make each new
keyframe by editing the nearest accepted frame, changing one thing (the pose, or the camera angle,
or the setting), at the exact resolution and aspect ratio of the clip; a mismatched input is
cropped or stretched, and the identity drifts with it. Write each edit as what stays, the one
change, and "keep the lighting, colour, camera and framing exactly as they are in the image": an
edit holds the existing light by reference and never re-describes it, because a description gets
re-rendered and the light shifts between keyframes. Describe light and camera like a photograph
only when generating a frame with no parent.
Inspect the whole body, not only the face.
When the same edit fails twice, change the picture (a closer parent, a smaller change), not the
adjectives.

A shot with more than one element (two people, a person with a prop in a place) gets a **staged
first frame**: the elements composed and lit together in one image, edited from their accepted
references, then used as the start frame. A person pasted onto a background reads as a cut-out and
animates like one.

## Prompt the motion only

The start frame already supplies the person, place, light and style. The prompt describes what
happens next in one or two present-tense sentences, then a **hold line** saying what must not
change:

```text
Good: The courier takes three unhurried steps toward the counter, the parcel swinging slightly in
      her right hand. Nothing else in the scene changes: no objects or people appear or disappear,
      her clothes and the parcel stay the same, and the lighting does not change. The camera stays
      still.

Bad:  Cinematic 8K shot of a beautiful courier in a detailed shop who walks over, smiles, puts the
      parcel down and looks around as the camera pushes in.
```

- **One motion per clip.** Walk, or turn, or sit, never all three; split at a rest point.
- **State movement as a change of position in the frame**: from where to where, how far ("from the
  doorway on the left to the desk at the centre, three steps"). A bare verb ("she moves", "drifts")
  comes back as bobbing in place. Check the subject actually moved before judging anything else.
- **Lock the camera** unless the shot is the camera move, and say so in every prompt; generators
  add drift on their own, and a drifting camera breaks the next join or cut.
- **End every prompt with the hold line**, and put the same list in the generator's negative-prompt
  field when it has one: no objects or people appear or disappear, clothing, hair and props do not
  change, the lighting does not change, the camera does not move. Generators fill time with
  invention, and things arriving from nowhere is their commonest continuity failure. Name the
  categories of change, not vivid specifics ("no new objects appear", not "no red balloon"): on a
  model without a negative channel a vivid noun can plant the thing it names.
- **Nothing arrives from nowhere.** Everything in the clip is already in the start frame, or enters
  by a visible route the brief names (a door, the frame edge).
- Reuse the same words for the person and setting in every clip.
- **Do not re-describe the light.** The start frame carries it; a prompt describing it invites the
  generator to relight the clip partway through, and the next join no longer matches.
- **Keep life in every clip**, holds and loops included: breathing, a blink, a small weight shift,
  cloth settling. A clip with no motion reads as a frozen still, and a generator asked for "no
  movement" often returns a slide-show or a sudden lurch.

## Direct natural human movement

People are where viewers see every error. A face that shifts, a foot that slides or an arm that
bends wrong reads as fake at once, even when the frame is beautiful. Direct the body as well as the
action:

- **Real speed.** Generators drift toward slow motion and floaty movement. State the pace ("at an
  unhurried walking pace", "quickly", "in about two seconds").
- **Weight and contact.** A planted foot stays planted while weight is on it, then lifts; feet never
  glide over the floor. A walk goes heel to toe with arms swinging opposite to the legs. Hands that
  touch something press on it or grip it.
- **Motion has a cause and an order.** A person shifts weight before stepping, looks before turning,
  reaches before grasping. Describe the movement in that order; a body that moves all at once moves
  like a puppet.
- **Keep the face toward the camera where you can.** Turns through profile and back are where
  identity drifts: the face that comes back is a stranger. Keep turns small, or end the clip in
  profile and check the face before continuing.
- **Keep the whole body in frame, or clearly out of it.** Hands and feet cut by the frame edge
  regrow wrong when they re-enter.

```text
Good: She shifts her weight onto her left foot and takes two unhurried steps toward the window,
      arms swinging naturally, then stops with both feet planted and breathes out.
Bad:  She gracefully glides to the window.
```

## Keep it subtle and human

Generators exaggerate: a smile becomes a grin, a glance becomes a head swing, a nod becomes a bow,
a step becomes a stride. Exaggeration is what makes footage read as generated, and a face pulled
into a big expression drifts away from the anchor. Default to small, and go big only when the brief
asks for it.

- **Give the size of every movement**: "a slight nod", "turns her head a little to the left", "lifts
  her hand to chest height". Unsized movement comes back large.
- **Show the person is human through small expressions**: a blink, a breath, a smile that forms
  slowly with the eyes softening, a brief look down and back up, brows lifting slightly. These carry
  emotion without pulling the face out of shape.
- **Leave out theatrical expressions** (open-mouth laughter, wide-eyed shock, hands to the face)
  unless the brief asks for them, and then give them their own clip and check the face against the
  anchor afterwards.
- **Emotion comes from the moment, not the volume**: a pause before the smile reads as more human
  than a bigger smile.

```text
Good: She looks up from the parcel and a small smile forms, her eyes softening, then she breathes
      out and gives a slight nod.
Bad:  She bursts into a huge happy smile and nods enthusiastically.
```

## Judge the whole clip

Endpoints that match prove the joins and nothing about the middle, where generation fails. For
every candidate:

1. Step through it at about one frame per second, and around every join or cut frame by frame.
2. Check each sampled frame against the anchor: the face; five fingers per hand; two arms, two
   legs and two feet attached and bending the right way; no limb through the body or an object;
   garments and props; objects in the scene (none appearing, vanishing or doubling); the light
   and colour holding steady, with no relight or exposure drift partway through; movements and
   expressions the size the brief asked for, not bigger.
3. Watch it at speed for the motion: one action, real speed, feet planted and not sliding, weight
   carried believably, blinks and breathing, no warping, no freeze.
4. Play it joined to its neighbours: a continuous join must be invisible, a reel cut must feel
   motivated.

Similarity scores between frames are a filter for gross failures, never acceptance; two frames can
score as near-identical while a hand has six fingers or a door has appeared.

Record every take in the log with its outcome. A clip that passes is kept and built on, never
regenerated; a later session that cannot see why a take failed generates it again.

```text
take  shot      parent frame          prompt ref  result    reason
t07   entry-02  entry-01 last (f143)  p-entry-02  rejected  parcel moves to left hand at 3 s
t08   entry-02  entry-01 last (f143)  p-entry-02  accepted  -
```

## Improve a miss

Name what failed and where (the second, the body part) before changing anything, then change one
thing in the next take:

| What failed | Next move |
|---|---|
| Face changes mid-clip | Shorter clip; smaller turn; keep the face toward camera and larger in frame; restart from an accepted frame |
| Hands, feet or limbs break during the action | Slow and simplify the action; describe it limb by limb; keep hands and feet in frame |
| Feet slide, body floats | State the pace and the steps; name where the weight goes and when feet plant |
| Nothing moves, or it reads as a still | Ask for small concrete life: breathing, blink, weight shift |
| Too much happens | One action per clip; split at a rest point |
| Garment or object pops in or changes | Shorter gap between start and end frame; remove the end frame; name the item in the prompt |
| Camera drifts | "The camera stays still" in every prompt; a start frame composed for the whole action |
| Jump at a continuous join | Re-extract the exact last frame; check size and rate match |

The same failure twice means change the frames or the plan, not the wording: a closer start frame,
a shorter step, the action split in two.

Read [improving takes](references/improving-takes.md) for each failure with a before and after
prompt, and prompts for entry, loop and exit clips.

## Use the generator's controls

Map the plan onto the generator's documented controls: start frame, end frame, mid-clip keyframes,
reference images, duration, resolution, and audio on or off. Check the current documentation for
the model in use; controls differ between models of the same provider. Read
[Grok Imagine](references/grok-imagine.md) when generating with xAI's video models, through their
API or an agent's built-in video tool.

## Stage, then install whole sequences

- Generate and judge candidates in a staging folder outside the shipped media. A half-finished
  sequence in the delivery folder ships half-finished.
- Normalize every accepted clip the same way: video stream only (audio, cover art and other
  attached streams removed), constant frame rate, the delivery size, codec and pixel format.
- Join clips by hard cuts. **No crossfades**: a dissolve shows two clips at half opacity, a visible
  ghost exactly where a continuous join should be invisible and a reel cut should be clean; a join
  that seems to need one has frames that do not match.
- Install a chain or reel only when all of its clips passed, then play it where it is used.

Read [frames and assembly](references/frames-and-assembly.md) for the commands before extracting a
frame, sampling a clip or joining clips.

## QC before calling it done

- [ ] A written plan and shot list preceded generation; every clip has a brief.
- [ ] The log has every take, with a reason for each rejection.
- [ ] Sampled middle frames pass the face, hands, feet, limbs, garments, props and scene checks.
- [ ] Every clip moves at real speed with planted feet and visible life; none reads as a still.
- [ ] Continuous joins are invisible and loops play three cycles without a hitch; reel cuts keep
      screen direction and feel motivated.
- [ ] No near-duplicate of an existing clip was added.
- [ ] Clips are normalized, joined by hard cuts, and installed as complete sequences.
- [ ] The installed footage was played where it is used.

Read [the source basis](references/sources.md) when changing a rule or checking a provider control.
