# Continuous chain

Read this before planning footage that must play as one unbroken view: a person entering, holding,
looping and leaving with no visible cut. Every clip starts on the real last frame of the clip
before it, so the joins are identical frames and the eye sees one shot.

## The rules that make it continuous

- **Start every clip on the real last frame** of the accepted clip before it, extracted exactly,
  never on a regenerated look-alike. A look-alike differs in a hundred small places, and every one
  jumps at the join.
- **Entry, loop, exit.** A hold is an entry clip that arrives at a rest pose, a loop that leaves and
  returns to that pose, and an exit that starts from it. The rest frame is shared by all three, so
  playback can switch at it.
- **A seamless loop uses the same frame at both ends**: first and last frame conditioned on one
  image. Two similar frames give a visible hitch every cycle.
- **Change place one human step at a time.** Moving the person to a new room or a distant spot is
  several clips, each covering what a person could do in a few seconds, each started on the real
  frame before it. Never pin a distant destination still as the end frame and let one clip
  interpolate: the generator melts the gap, so objects pop in, garments change, doors double and
  limbs pass through furniture. Use an end frame only when it is a few seconds of plausible motion
  from the start frame.
- **Keep chains short.** Each generation from a generated frame drifts a little further: colour,
  light and face. When a sequence needs more than a handful of links, plan a cut and re-start the
  next part from an accepted keyframe; that part is then a reel, not a continuous shot.

## The workflow

1. **Anchor and rest frame.** Make the rest frame by editing the person's anchor still into the
   rest pose, at the delivery resolution and aspect ratio. Inspect it whole.
2. **Plan the chain** on paper: every clip with its brief, start frame, end frame (usually free),
   and the one motion it does. Mark which clips are loops.
3. **Generate the first clip** from its keyframe. Judge it through the middle, not only the ends.
4. **Accept or log the rejection.** A rejected take is regenerated from the same start frame; never
   from a frame of the rejected take.
5. **Extract the exact last frame** of the accepted clip: count the decoded frames, then select
   frame N−1. An approximate seek near the end lands a frame or more early, and the next clip starts
   out of step: a visible jump at the join. The commands are in
   [frames and assembly](frames-and-assembly.md).
6. **Check the extracted frame**: its size equals the clip's, it matches the clip's final frame
   stepped in a player, and it still matches the anchor. A frame that has drifted from the anchor
   passes the drift to every clip after it; stop and fix that clip first.
7. **Generate the next clip from that frame.** Repeat steps 3 to 7 down the chain.
8. **Continue what passed.** When an entry passes and its exit fails, generate a new exit from the
   entry's extracted last frame; do not refilm the entry. Regenerating a passing clip spends
   attempts and throws away a known-good join.
9. **Make the loop's rest frame real.** The entry rarely ends exactly on the planned rest frame. Use
   the entry's accepted last frame as the rest frame, so the loop and the exit start where the
   entry really ended, and condition both ends of the loop on it.
10. **Join** with hard cuts, dropping the duplicated join frame from one side; count the joined
    frames against the sum of the parts. Play every join frame by frame, then the whole chain at
    speed, loops for three cycles.
11. **Install the complete chain** and play it where it is used.

## An example chain

```text
anchor   accepted still of the receptionist, standing, 16:9 at delivery size
K0       edit of anchor: she stands in the doorway, left of frame
entry-01 start K0, free end: she walks in at an unhurried pace and stops behind the desk
R        = exact last frame of entry-01 (accepted)
loop-01  start R, end R: she breathes, blinks, glances down at the desk and back up
exit-01  start R, free end: she turns to her left and walks out of frame
playback entry-01 → loop-01 × n → exit-01, hard cuts on R
```
