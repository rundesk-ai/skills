+++
skill = "writing-manuscripts"
kind = "quality"
difficulty = "medium"
fixture = "lena"
protect = ["The road was empty. Good.", "*He always does this,* she thought. *Always.*", "The sea was the colour of a knife.", "\"You said come.\""]
rubric = """
result.1  "Thomas" becomes "Tomas", and "older brother" becomes "younger" or is queried, against the reference sheet.
result.2  "10 minutes" becomes "ten minutes" (numbers as words).
result.3  The present-tense paragraph ("She parks… walks… is sitting") is returned to past tense.
result.4  The point-of-view slip ("Tomas thought she looked tired") is flagged or fixed without inventing new content, and the two-hour drive taking "Forty minutes" is queried or flagged, not silently rewritten to a new number.
result.5  Keeps the fragments ("Good."), the italic thoughts and British spelling ("colour"), and changes nothing beyond copyediting.
conduct.1 Checks the chapter against reference.md and reports each inconsistency with what settled it or a question.
"""
+++
Please copyedit chapter-7.md against my reference sheet (reference.md). Make the fixes in the file and tell me what you changed.
