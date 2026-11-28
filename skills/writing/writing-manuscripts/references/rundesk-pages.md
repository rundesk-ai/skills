# Rundesk pages

Read this when the manuscript is kept in Rundesk's Pages tab. It covers where the manuscript sits,
how its order works and how to format a sheet so it reads and prints well; the editing rules in the
skill are unchanged.

## Where the manuscript is

- **Sheets are markdown files.** A project's Pages tab shows the sheets in its `pages/` folder, or in
  the folder its `desk.yml` names under `pages:`. Each sheet is usually one chapter, scene or note.
  A folder is a chapter or a part; a folder inside a folder is a section.
- **Edit only the sheets you were asked about.** A sheet the writer didn't name may be a draft they
  abandoned or a scene they haven't reached; reading it for continuity and style is fine, changing
  it is not.
- **Reference sheets are the truth.** When the project has sheets for characters, places, a timeline
  or a series bible, check the chapter against them, and report a disagreement instead of editing
  either one to match the other.
- **Sheets are not docs.** Rules a project sets for its documentation, such as citations, a docs
  check or a docs index, never apply to the manuscript's sheets.

## How writers usually lay out a book

These are the common patterns, not rules. Read the writer's own structure first and follow it.

- **A top-level sheet is its own printed page or pages** in Read and the PDF: a title page, a
  dedication, a foreword, or a chapter written as one sheet.
- **Folders are usually chapters or parts, and the sheets inside a chapter folder are usually its
  scenes,** which run on together as one chapter. A writer splits a chapter into scenes so each one
  can be worked on, reordered and moved on its own.
- **Not every folder is the story.** Writers also keep notes, research, outlines, character sheets
  or drafts in folders and sheets of their own. Never assume a folder is a chapter or a sheet is a
  scene: a folder of notes is not part of the manuscript, and edits, chapter counts and page breaks
  leave it alone. When you can't tell whether a folder belongs to the book, ask.
- **What follows from this.** To start a chapter on a new page, make it a top-level folder or sheet.
  To add a scene, add a sheet in the chapter's folder, at its place in the order. To split a long
  chapter sheet into scenes, propose it first, because it changes the writer's structure; then move
  the text into the new sheets without rewording it.

## How the order works

- **The order lives in a hidden `.order` file in each folder,** one file or folder name per line.
  Lines starting with `#` and blank lines are ignored. Names the file doesn't list come after the
  listed ones, sorted by file name. In a folder with no `.order`, a `01-` style prefix still orders
  the files.
- **File names are fixed.** Sheets made in Rundesk are named `sheet-<13-digit time>-<3 letters>.md`,
  and the name never follows the title. Never rename a file to retitle or reorder it: other sheets
  and the writer's links point at the name.
- **To read the manuscript in order,** use Rundesk's tools for listing the sheets or reading the
  manuscript in order when they are available to you; otherwise read each folder's `.order`, then
  the unlisted names in file-name order. Read the sheets around the one you edit in that order, not
  in file-name order.
- **To reorder,** use Rundesk's tool for moving a sheet when it is available (it reorders within a
  folder); otherwise edit the folder's `.order`, moving only the lines that change.
- **When you move a sheet or a chapter, fix the links your move broke.** Rundesk rewrites no links,
  so search every sheet, notes included, for links to the old path and change only the link target
  to the new one, never the link text or anything around it. List each change (which sheet, old
  path, new path) so the writer can undo it. This is a mechanical path fix, not an edit of their
  words. A broken link you didn't cause is reported, not fixed.

## How to format a sheet

Rundesk saves exactly what was typed, so match the writer's markdown and add nothing for layout.

- **A sheet's name is its first line.** A chapter or scene sheet opens with its heading
  (`# Chapter One`) or a plain first line, never a blank line, and never front matter the writer
  didn't put there. To retitle a sheet, edit its first line, not the file name. The title is the
  writer's: suggest a new one in the report unless they asked for the change.
- **Leave front matter alone.** The block between `---` lines at the top of a sheet is hidden by
  Rundesk and belongs to the app and the writer; edit the body below it, and when the sheet has
  front matter, its name is the first line after it.
- **Paragraphs are one blank line apart, and that's all.** The editor sets book-style paragraphs
  itself (first-line indents, no gap between paragraphs, none after a heading), so never type
  indents, extra blank lines or non-breaking spaces for layout.
- **A scene break is `***` on its own line.** The sheets in a folder run on as one in Read and in the
  export, with nothing added between them, so a break between two sheets is a `***` the writer
  puts there: at the end of the earlier sheet, because the later sheet's first line is its name.
  Don't add a break the writer didn't ask for.
- **Keep the writer's markdown style.** `_italic_` stays `_italic_` and `*italic*` stays `*italic*`;
  a writer who breaks scenes with `---` keeps `---`; footnotes stay `[^1]`. Converting one style to
  another changes every line it touches and the writer's file with it.
- **Page breaks follow the structure.** In the printed PDF each top-level sheet and each top-level
  folder starts a new page, and sections (folders in folders) run on. A title page is a top-level
  sheet; a chapter is a top-level folder or sheet. To start a chapter on a new page, place it at the
  top level rather than adding a break by hand.
