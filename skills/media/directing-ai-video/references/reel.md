# Reel

Read this before planning a short sequence of shots joined by cuts: a reel, a teaser, a scene told
from several angles. A cut is allowed here, but it must feel motivated: the viewer should feel the
story moved, not that the footage broke. Film editing has a grammar for that, and the generator
knows none of it; the director applies it in the plan.

## Plan the scene first

1. **One sentence of story.** What happens, to whom, and what the viewer should feel at the end.
   "The baker opens the shop at dawn and the first customer is her old teacher" is a scene; "nice
   shots of a bakery" is not.
2. **Beats.** Break the sentence into three to eight beats, one action each. Each beat becomes one
   shot, sometimes two.
3. **Shot list.** For every shot: number, size (wide, medium, close-up), angle, the person's one
   action, screen direction, duration, and **why the cut to the next shot happens** (an action
   completes, a look, a sound, a reveal). A cut with no reason is the one that feels wrong.
4. **Continuity sheet.** The person's identity card, outfit and props per shot, time of day, light
   direction, and a palette of three to five colours repeated in every prompt. Most broken reels
   break here: the jacket is open in one shot and closed in the next.
5. **Show the plan** to whoever owns the footage before generating.

## Cut grammar

- **Open wide, then move closer.** An establishing wide shot tells the viewer where they are;
  medium and close shots then read without confusion. Coming back out to a wide resets the space.
- **Change size or angle enough at every cut.** Two consecutive shots of the same person need a
  clear change: a different shot size, or a camera angle at least about 30 degrees apart. A small
  change reads as a jump cut, the person twitching in place.
- **Keep screen direction.** Keep the camera on one side of the line of action (the 180-degree
  rule). A person who exits frame right enters the next shot from frame left; a person looking
  right in one shot is looked at from the left in the reverse. Crossing the line flips the
  geography, and the viewer loses who is where.
- **Cut on action.** End a shot mid-movement and start the next on the same movement from the new
  angle: she reaches for the door handle in the wide, her hand closes on it in the close-up. The
  movement carries the eye across the cut.
- **Match the eye.** Put the next shot's point of interest near where the viewer was already
  looking at the cut; a cut that makes the eye search the frame feels like a jolt.
- **Emotion and story outrank geometry.** When a cut cannot satisfy every rule, keep the one that
  serves the feeling and the story, and let a small spatial mismatch go.

## Making each shot

- **Every shot's start frame descends from the anchor**, edited to the new angle or size, one change
  per edit, at the delivery resolution and aspect ratio. A new angle generated from text is a new
  person.
- **For a cut on action**, make shot B's start frame by editing shot A's accepted last frame: same
  pose and moment, only the camera angle or size changes. Then generate B continuing the motion.
- **Same light and palette in every shot.** Restate the light direction and colours in each prompt;
  consistent lighting logic is what makes a cut seamless.
- **One shot, one action, one camera move at most.** A shot that also has to move the camera is
  still one shot with one subject action.
- **Trim to the action.** A clip generated from a still often starts static and drifts at the end.
  Cut in after the movement has begun and out before it settles or drifts; the cut points are
  chosen in the edit, not taken from the clip's ends.
- **Rhythm.** Hold a shot as long as its action needs and no longer, typically a few seconds. Vary
  durations; a reel of equal shots plods. Cut on the beat of the action, not on a timer.

## Assemble and review

Join with hard cuts, no dissolves. Watch the whole reel at speed, several times, then each cut
frame by frame: same person, same outfit and props, screen direction kept, motion continuing across
cut-on-action pairs, light consistent. Fix a failing cut by regenerating or re-trimming one shot,
never by adding a transition to hide it.

## An example shot list

```text
Story: the courier delivers the last parcel of the day and finally sits down.
Light: late afternoon, warm, from frame left. Palette: navy, mustard, warm grey, brick.

#  size    angle            action                                   dir   dur  cut because
1  wide    eye level, side  she walks along the street, left to right L→R   3 s  she reaches the shop door
2  medium  front, 3/4       she pushes the door open and steps in     L→R   3 s  cut on the door swing
3  close   over shoulder    she sets the parcel on the counter        -     2 s  the parcel lands
4  medium  front            she exhales and smiles at the clerk       -     3 s  her look off frame right
5  wide    eye level, side  she sits on the bench by the window       L→R   4 s  end: she leans back
```

Shot 2's start frame is an edit of shot 1's last frame, the camera moved to the front three-quarter
angle; shot 5 returns to shot 1's side angle, so the street geography holds.
