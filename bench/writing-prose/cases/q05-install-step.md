+++
skill = "writing-prose"
kind = "quality"
difficulty = "easy"
rubric = """
result.1  Keeps every fact: signed with a Developer ID, notarized by Apple, the notarization ticket is stapled to (travels with) the DMG, so it opens even offline; needs macOS 14 or later; drag the app to Applications; the first launch asks to allow access to the Documents folder.
result.2  The reader is the actor in the steps ("Open the DMG and drag…", "you'll see…"), and the signing paragraph says why it matters to the reader (no warning, works offline).
result.3  No three sentences in a row open on the same subject; related facts are joined (so, because, then) rather than stacked.
result.4  Keeps the natural phrase "even when you're offline" or an equally plain one; does not swap it for a formal one ("without a network connection", "in the absence of connectivity").
result.5  Invents nothing: no version number, file size, menu path or permission the draft does not give.
conduct.1 Contractions or a plain conversational register appear where natural, with no hype ("seamless", "effortless", exclamation marks) or padding ("simply", "just", "in order to").
"""
+++
Tighten this install step for our public docs. Readers are installing Tidepool on a Mac for the first time.

> ## Install on macOS
>
> Tidepool requires macOS 14 or later. The DMG is signed with a Developer ID. Apple has notarized the DMG. The notarization ticket is stapled to the DMG. The DMG opens without a network connection. Open the DMG. Drag Tidepool to the Applications folder. On first launch, Tidepool requests access to the Documents folder. Access must be allowed for sync to work.
