# Improving takes

Read this when a clip failed judging, or before writing prompts for a chain. Each failure has a
symptom, the cause, and a before and after prompt. The character throughout is an invented one: a
receptionist in a navy blazer, standing behind a reception desk, camera locked at chest height.

## Diagnose before rewording

Write down the second and the body part: "at 2.5 s her right hand gains a sixth finger as she lifts
the pen", not "the hands look weird". Change one thing in the next take, so the take tests one idea.

## Face changes mid-clip

She turns to look at the door and turns back as someone else. The model has to invent the unseen
side of the face, and longer clips drift further from the start frame.

```text
Before: She turns around to look at the clock behind her, then turns back and smiles.
After:  She turns her head a little to her right to glance at the door, then looks back at the
        camera with a small closed-mouth smile. The camera stays still.
```

Keep the face toward the camera and large enough in frame to hold detail. When a shot must show a
full turn, end the clip in profile, check the face against the anchor, and start the next clip from
that frame.

## Hands break during an action

The pen passes through her fingers; a hand merges with the desk. Fast, complex hand actions are the
hardest motion to generate.

```text
Before: She picks up the pen, signs the form and hands it over.
After:  She picks up the pen from the desk with her right hand, fingers closing around it, and
        brings it to the form. The camera stays still.
```

Signing and handing over are the next two clips. Keep both hands in frame for the whole clip.

## Feet slide, the body floats

She drifts across the floor with no steps, or her feet skate under her. The prompt gave a
destination, not a walk.

```text
Before: She moves to the end of the desk.
After:  She takes three unhurried steps to her left along the desk, each foot planting flat before
        the next lifts, arms swinging slightly, and stops with her weight on both feet.
```

Frame the shot so the feet are either clearly visible or cleanly out of frame, not cut at the edge.

## Slow motion or dreamy movement

Everything moves as if underwater. Many generators default to slow, smooth motion when the pace is
unstated.

```text
Before: She waves hello.
After:  She raises her right hand to shoulder height and gives two quick waves, then lowers it,
        all in about two seconds.
```

## It reads as a still

The loop or rest hold looks like a photograph, or the generator jumps to sudden motion to fill the
time. The prompt asked for nothing, or for "no movement".

```text
Before: She stands still behind the desk.
After:  She stands behind the desk, breathing slowly, blinking now and then, shifting her weight
        gently from one foot to the other. The camera stays still.
```

## Something pops in or changes

A vase appears on the desk at 3 s; the blazer gains a pocket; a second door opens in the wall. The
end frame was too far from the start frame, and the model filled the gap with invention.

End the prompt with the hold line ("Nothing else in the scene changes: no objects or people appear
or disappear ..."), and put it in the negative-prompt field when there is one. Then remove the end
frame, or replace it with one a few seconds of plausible motion away. When the clip
must reach a distant state, add clips between: each starts on the previous real last frame.

## Movement or expression too big

She was asked to smile and grins; asked to look at the door and swings her whole head. Unsized
movement comes back large.

```text
Before: She smiles and looks at the door.
After:  A small closed-mouth smile forms as she glances a little to her right toward the door, then
        her eyes come back to the camera. Nothing else in the scene changes. The camera stays still.
```

## The camera drifts

A slow push-in nobody asked for, or a pan that leaves the subject. Many models add camera motion
unless told otherwise, and a prompt rewriter may add it on purpose.

End every prompt with "The camera stays still." When a provider has a prompt-enhancement option,
check whether it rewrote the camera.

## Prompts for a chain

Rest frame R: she stands behind the desk facing the camera, hands resting on the desk.

```text
Entry (start: doorway keyframe, end: free):
  She walks in from the left at an unhurried pace, steps behind the desk and stops facing the
  camera, resting both hands on the desk. The camera stays still.

Loop (start: R, end: R):
  She breathes slowly and blinks, glances down at the desk and back up at the camera, her hands
  resting on the desk. Nothing else in the scene changes. The camera stays still.

Exit (start: R, end: free):
  She lifts her hands from the desk, turns to her left and walks out of frame at an unhurried pace.
  Nothing else in the scene changes. The camera stays still.
```

The entry rarely ends exactly on R. Make R from the entry's accepted last frame, so the loop and
the exit start where the entry really ended.
