+++
skill = "directing-ai-video"
cases_version = 1
kind = "quality"
difficulty = "easy"
rubric = """
result.1  Extracts the exact last decoded frame by frame index: counts decoded frames (for example ffprobe -count_frames), then selects frame N-1 counting from zero; does not rely on -sseof or a time seek near the end.
result.2  Saves the frame losslessly (PNG) at the clip's own size and uses it as the next clip's first frame.
result.3  Explains why an approximate seek causes a visible jump at the join.
conduct.1 Says how to confirm the extracted frame is the clip's final frame.
"""
+++
The generator accepts a start image. I want clip 2 to continue exactly where clip1.mp4 ends, with no jump at the cut. Give me the commands to get the start image for clip 2.
