+++
skill = "directing-character-images"
cases_version = 1
kind = "quality"
difficulty = "complex"
rubric = """
result.1  Stops rewording: two misses on the same edit mean change the input picture (closer parent, smaller step, crop and edit the region, a pose or garment reference, recompose so the hand is out of frame).
result.2  Diagnoses that naming "freckles" in every prompt is amplifying them, and removes the word, letting the reference carry the trait.
result.3  Returns to the accepted anchor or the last accepted image rather than continuing from the drifted one.
result.4  Keeps a record of accepted images with their parent and prompt, and rejected takes with their reasons.
conduct.1 Separates what it can say from the description from what needs another generation run to confirm.
"""
+++
I have been editing the same image of our character for an hour. I have asked six times, with different words each time, for her left hand to hold the cup by the handle, and it keeps coming out with fused fingers. Meanwhile her freckles have got much stronger and her face looks older than in the original. Every prompt says "keep her freckles". What am I doing wrong and what should I do now?
