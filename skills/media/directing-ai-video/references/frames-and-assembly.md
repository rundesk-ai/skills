# Frames and assembly

Commands use ffmpeg and ffprobe, the common command-line tools; any tool that decodes every frame
and reports its index does the same job. Check the installed version's documentation when an
option is refused.

## Extract the exact last frame

Count decoded frames first. The container's stored frame count can be missing or wrong; decoding
every frame is slower and correct.

```sh
N=$(ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=nb_read_frames -of csv=p=0 clip.mp4)
ffmpeg -v error -i clip.mp4 -vf "select=eq(n\,$((N-1)))" -fps_mode passthrough \
  -frames:v 1 last.png
```

- `n` counts decoded frames from zero, so the last one is `N-1`.
- Save as PNG: a lossless still, so the next clip starts from the pixels the viewer saw, not a
  re-compressed copy.
- Do not use a time seek near the end (`-sseof`, or `-ss` with the duration). A seek targets a
  time, not a frame index; rounding, variable frame timing or an end-of-stream edge case picks a
  neighbouring frame or none, and the next clip starts out of step.
- Confirm the result: compare `last.png` with the clip's final frame stepped in a player, and check
  its size equals the clip's frame size.

Extract a first frame the same way with `eq(n\,0)`; it is the check that a loop starts where it
ends.

## Sample the middle for judging

```sh
ffmpeg -v error -i clip.mp4 -vf "fps=1" sample-%03d.png             # one frame per second
ffmpeg -v error -i clip.mp4 -vf "select=gte(n\,$((N-6)))" -fps_mode passthrough tail-%02d.png
```

Lay the samples side by side with the anchor still, or tile them into one contact sheet with the
`tile` filter, and inspect at full size.

## Normalize every clip

```sh
ffmpeg -v error -i take.mp4 -map 0:v:0 -an -sn -dn -map_metadata -1 \
  -vf "scale=1920:1080:flags=lanczos,fps=24,format=yuv420p" -fps_mode cfr \
  -c:v libx264 -crf 16 -preset slow clip.mp4
```

- `-map 0:v:0` keeps only the first video stream; `-an -sn -dn` drop audio, subtitle and data
  streams, which also drops attached cover images.
- `fps=24` and `-fps_mode cfr` give every clip the same constant rate, so joins line up frame for
  frame. Use the delivery's rate and size, the same for every clip in the chain.
- Normalize before extracting a frame for the next clip only when the next clip is generated from
  the normalized file; otherwise extract from the take that was judged.

## Join a chain with hard cuts

When adjacent clips share the join frame, drop it from one side so it is not shown twice (a
one-frame hold reads as a stutter): trim the first frame of each clip after the first.

```sh
ffmpeg -v error -i entry-02.mp4 -vf "select=gte(n\,1),setpts=N/FRAME_RATE/TB" -fps_mode cfr \
  -an -c:v libx264 -crf 16 entry-02.trim.mp4
printf "file '%s'\n" entry-01.mp4 entry-02.trim.mp4 loop-01.trim.mp4 > chain.txt
ffmpeg -v error -f concat -safe 0 -i chain.txt -c copy chain.mp4
```

Stream copy (`-c copy`) is valid only when every input has the same codec, size, rate and pixel
format, which normalizing guarantees. Count the joined file's frames: it must equal the sum of the
parts.

For a loop played by a player that repeats it, ship the loop with its last frame removed, so the
shared frame appears once per cycle.
