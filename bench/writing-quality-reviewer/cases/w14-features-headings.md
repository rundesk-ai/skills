+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "features-page"
cases_version = 3
key = """
must:
  M1 headings   The headings don't say what their feature is when read alone: "Break it into pieces" and "Take it anywhere" (pronoun with no noun), "Know where you stand" and "Yours, always" (riddles the body decodes). Reported with every place and a replacement built from that section's own body (for example "Live word count and reading time", "Export to PDF or EPUB").
  M2 first line "It works offline, and your files are plain Markdown on your own disk." leans on its heading for "It"; the fix names Inkwell.
  M4 columns    The plan table's column headers "What it does" and "Who it's for" name the row's subject by pronoun; replacements name what each column holds (for example "Includes", "Best for").
  M3 overreach  "and nothing else moves" has no source in FACTS.md and no clear meaning; cut it or ask what it promises.
decoys (not findings):
  D1 Claims that match FACTS.md (chapter files, drag to reorder, live counts and reading time, 90 days of history, distraction-free mode, PDF and EPUB, offline Markdown).
  D2 The list shape: a features section is a list by form.
  D3 Short heading-plus-sentence blocks as a cadence problem.
  D4 The "Compare plans" heading and the "Plan" column: both stand alone.
taste:
  T1 "Just you and the page": a mood more than a name, but it can be read as distraction-free mode; flagging it or leaving it are both fine.
  T2 The title "Write the book. Inkwell handles the rest."
extras:
  X1 "Never lose a good line" against the 90-day limit, or as a heading that doesn't name version history.
  X2 "Take it anywhere" suggesting sync or a mobile app the facts don't list.
  X3 a replacement heading that adds a feature, number or claim not in FACTS.md.
"""
+++
Review features.md, the features section of our landing page, before it goes live. FACTS.md has the confirmed features.
