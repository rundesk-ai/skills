# Improving takes

Read this when a candidate failed inspection, or before a difficult edit. Each failure has a
symptom, the cause, and a before and after prompt. The character throughout is an invented one:
a chef, broad build, about fifty, short grey beard, white double-breasted jacket, navy apron,
silver watch on the left wrist.

## Diagnose before rewording

Write one line on what failed and which category it is, before touching the prompt. "Looks off" is
not a diagnosis; "beard is shorter and darker than the anchor" is. Change one thing in the next
attempt, so the attempt tests one idea.

## The change did not happen

The model returned nearly the same image. The change was abstract, buried among keep instructions,
or too large to take in one step.

```text
Before: Keep everything the same but make him look like he's finished cooking.
After:  Keep: the same man, same face, short grey beard, white double-breasted jacket, navy apron,
        silver watch on his left wrist, same kitchen and lighting.
        Change: he lays the knife flat on the cutting board and rests both hands on the counter
        edge either side of the board.
        Keep everything else in the image exactly as it is.
```

## Identity drifted with the change

The new pose came with a new face. A large pose change pulls the model away from the reference.

```text
Before: Turn him around so he's facing the stove at the back of the kitchen and reaching up for a pan.
After (step 1): ... Change: he turns his head and shoulders a quarter to his left, toward the stove;
                his feet stay where they are.
After (step 2, from the accepted step 1): ... Change: he raises his right arm to the pan rail above
                the stove, fingers closed around the handle of a steel pan.
```

When the tool takes several images, send the anchor as image 1 with the job "the man's face and
build", and the current image as image 2 with the job "the scene and pose to edit".

## Identity drifted over many edits

Each edit looked fine against its parent, but the tenth image is a different person. Small errors
compound when every edit starts from the previous output.

Compare every candidate with the anchor, not only with its parent. When it has drifted, go back to
the last image that still matches the anchor and redo the later edits from there, or put the anchor
back in as the identity reference.

## A trait grew stronger

The beard got bushier with each edit; freckles darkened; a nose grew. The prompt kept naming the
trait, and naming is a request for more of it.

```text
Before: Keep his distinctive thick grey beard and weathered face. Change: he smiles.
After:  Keep: the same man, same face and beard as the reference, same jacket and apron.
        Change: he smiles with his mouth closed, eyes slightly narrowed.
```

Then edit from the last image where the trait was right, not from the exaggerated one.

## Hands or limbs broken

Fused or extra fingers, a hand that floats beside the object, an elbow bending backwards. Hands are
small, articulated and often occluded, and models still fail on them measurably.

```text
Before: He holds the cup properly, normal hand, five fingers.
After:  Change: his right hand holds the white mug by its handle, index and middle fingers through
        the handle, thumb resting on top, the mug at chest height.
```

When two attempts fail: crop to the hand and forearm, edit only that region, and composite it back;
supply a reference photo of the grip with the job "hand pose only"; or recompose so the mug hides
most of the hand.

## Feet, toes or proportions wrong

Six toes, two left feet, a foot sunk into the floor, legs of different lengths, a head too large
for the body. Feet and proportions are rarely named and rarely checked, so they fail silently.

```text
Before: Full body shot of him standing barefoot on the beach.
After:  Change: he stands barefoot on firm wet sand, feet hip-width apart and pointing forward,
        weight on both feet, toes visible at the edge of the frame's lower third.
```

When proportions drift, edit from the anchor with the full body in frame, and check the head, arm
length and leg length against it with both images at the same height.

## A pose no body could hold

He leans with nothing behind him, sits on air, or balances on one heel. The model drew the pose
without the support that makes it possible. Name the support.

```text
Before: He leans casually.
After:  Change: he leans his right shoulder against the door frame, weight on his right leg, left
        foot crossed in front of the right.
```

## Outfit or prop changed

Buttons became a zip, the apron turned black, the watch moved wrists. The prompt named the garment
generically or not at all.

```text
Before: Keep his chef clothes.
After:  Keep: white double-breasted jacket with two rows of three cloth buttons, sleeves rolled to
        the forearm, navy apron tied at the waist, silver watch on his left wrist.
```

When a garment keeps changing, pass a clean image of it as a second reference with the job "the
jacket only".

## Lighting changed

The edit came back relit: the light moved to the other side, warmed, or flattened, though the
prompt asked to keep it. The prompt described the light, and the model rendered its own version of
the description instead of the light in the image.

```text
Before: Keep: the same man, ..., warm tungsten light from the window on the left, moody kitchen.
        Change: he wipes his hands on his apron.
After:  Keep: the same man, same face and beard, same jacket, apron and watch.
        Change: he wipes both hands on the front of his apron.
        Keep the lighting, colour, camera angle, framing and background exactly as they are in the
        image.
```

Compare the shadows under the chin and nose and on the wall with the parent: they are the first
place a relight shows.

## Something else changed too

The background redrew, the light flipped sides, a sign with garbled text appeared. The prompt left
those elements unnamed, or asked for a mood ("warmer", "more cinematic") that the model applied to
everything.

```text
Before: Make it more cinematic.
After:  Keep the man, his outfit and pose exactly. Change: the light becomes warm and low, coming
        from a window on the left; the back wall falls into soft shadow.
```

Style words are not changes. Translate each into the physical thing it means (light direction and
colour, camera height, lens length, depth of field) and make that the one change.

## A worked sequence

Target: the chef at a market stall, holding a crate of tomatoes, 9:16, to start a video clip.

1. **Anchor** (from the reference photo, 9:16): "The same man as the reference photo, standing
   facing the camera, arms relaxed at his sides, in a white double-breasted jacket and navy apron,
   silver watch on his left wrist, against a plain light grey wall, even soft light." Inspect.
2. **Scene**: "Keep: the same man, face, beard, build, jacket, apron, watch, pose. Change: he stands
   behind a wooden market stall stacked with vegetables, outdoors in overcast daylight. Keep
   everything else exactly as it is." This is a new setting, so its light is part of the change and
   is described once, here; later edits hold it by reference. Inspect: face against the anchor,
   hands, stall scale.
3. **Prop and pose**: "Keep: the same man, face, beard, outfit. Change: he holds a shallow
   wooden crate of tomatoes in front of his waist, one hand on each short side, fingers under the
   rim. Keep the lighting, stall, camera and framing exactly as they are in the image." Inspect hands
   first, then the light against step 2.
4. If step 3 fails twice: crop to the torso and edit the crate and hands there, or use a photo of
   hands holding a crate as a pose reference. Do not reword step 3 a third time.
5. Record the accepted chain: anchor → scene → crate, each with its prompt, and the rejected takes
   with their reasons.
