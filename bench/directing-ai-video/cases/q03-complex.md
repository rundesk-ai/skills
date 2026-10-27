+++
skill = "directing-ai-video"
cases_version = 1
kind = "quality"
difficulty = "complex"
rubric = """
result.1  Keeps the passing entry and generates new exit takes from the entry's real extracted last frame, rather than refilming the entry.
result.2  Fixes the loop hitch by conditioning the loop's first and last frame on the same image (the entry's rest frame), not two similar frames.
result.3  Declines the crossfade: hard cuts on the shared frame, because a dissolve shows a ghost where the join should be invisible.
result.4  Adds life to the loop (breathing, a small weight shift) so the hold does not read as a still.
result.5  Installs only a complete chain after QC, staging candidates outside the shipped media; notes that ending with nothing installed is a failure.
conduct.1 Keeps a take log with a rejection reason for each failed take.
conduct.2 Separates what it established from what still needs a generator run to verify.
"""
+++
State of the hero video: entry.mp4 (the host walks in and stops at the desk) looks great. The loop clip has a small hitch every cycle and she stands so still it looks like a photo. All five exit takes have her coat changing colour. The designer suggests refilming everything as one long clip and putting 0.5 s crossfades between the parts to hide the joins. We ship tomorrow. What should we do?
