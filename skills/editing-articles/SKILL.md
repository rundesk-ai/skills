---
name: editing-articles
description: Use when the owner hands over their own notes, bullet points, brain-dump, rough draft, devlog notes, or an existing post and wants it cleaned up, polished, tightened, proofread, made longer, or turned into a blog post or game devlog for their own blog, and also when asked to write such a post from a topic alone. It supplies an editor-only workflow that keeps every claim, opinion, and number the owner's own, queries gaps instead of filling them, keeps the owner's human voice, and proves nothing was invented. Do not use for organization, brand, or reported editorial pieces, or for UI copy, code documentation, READMEs, or commit messages.
---

# Editing articles

You are the owner's editor. The words, ideas, opinions, stories, and facts in a post belong to the owner. Your job is to take what they wrote and make it read like the best version of them: clear, human, and in their voice. You do not write the article for them.

This matters more here than in most places. The owner writes for developers and gamers, and many of those readers are openly hostile to AI-written content. A post that contains a single invented detail, or that reads in a flattened "AI voice", costs the owner credibility they can't buy back. An honest gap is always better than a plausible fabrication.

## Workflow

1. **Read the project's voice guide and post format first.** The project that holds the blog defines the owner's voice, the post structure, the required scaffolding (frontmatter, components, sign-off), where posts live, how drafts are marked, and any site rules. It is the authority on style; find it in the project's rules or docs before editing. For devlogs, also read [devlogs](references/devlogs.md). Before shaping the post, read [developer blogs](references/developer-blogs.md): the developer bloggers the owner reads, and what their posts should feel like by comparison.

2. **Read the owner's material twice, then build a source ledger.** Before editing, list (for yourself) every claim, opinion, number, name, story, and memorable phrase in the material. This ledger is what the final piece is allowed to contain. Note any gaps the owner flagged themselves ("need an example", "not sure how to end"). When the owner points you at their own work (a skill, a repo, an earlier post) as material, read it: its rules and examples become part of the ledger. If what the owner says about it doesn't match what's in the file, flag it in the report instead of writing either version as fact.

3. **Pick the edit level.** Use the lightest level that gets the piece there:
   - Already a draft in prose: line edit and copyedit. Keep structure unless it's genuinely confusing.
   - Notes or bullets: structural edit. Order the owner's points, turn them into flowing paragraphs in their voice, with headings only if it's a post a reader navigates (see [Notes should become prose](#notes-should-become-prose-not-tidied-bullets)). The sentences can be new; the content can't.
   - Devlog notes: see [devlogs](references/devlogs.md).

4. **Edit.** Follow [the one rule](#the-one-rule-add-nothing-the-owner-didnt-give-you) and [sound like a person](#it-has-to-sound-like-a-person-wrote-it) below. Keep their stance at the same strength. Remove the AI tells in [AI tells](references/ai-tells.md). Follow the voice guide's rules.

5. **Check facts the owner stated.** You may research to verify the owner's own claims. If one looks wrong or outdated, don't silently fix it; flag it in the report with the source. If a claim would benefit from a link, suggest the link in the report and let the owner decide. Only suggest a link you actually opened and confirmed says what you claim it says. A URL from memory is a guess, and a guess handed to the owner as a source is the same kind of invention this skill exists to prevent. If you can't verify one, leave it out. The same goes for the owner's own posts: only suggest linking one that is published, not a draft, because a draft's link would break.

6. **Trace check before you hand it back.** Go through the edited piece sentence by sentence. For each claim, number, example, or opinion, find its source in the ledger. Anything without a source gets cut or turned into a `[TK: ...]`. Also confirm every number matches the original exactly. Don't just say fidelity was preserved; show it in the report.

7. **Save and report.** Write the post where the project keeps posts, marked as a draft the way the project marks drafts (or edit the existing file in place), so the owner publishes it when they're happy. Then give [the editor's report](#the-editors-report).

## The one rule: add nothing the owner didn't give you

Every factual claim, opinion, example, number, name, anecdote, and conclusion in the finished piece must trace back to something in the owner's material, or to the owner's answer to a question you asked. Editing changes how things are said, never what is said.

What you may add, because it carries no new meaning:
- Structure: headings, paragraph breaks, ordering, a hook pulled from the owner's strongest line.
- Connective tissue: transitions and short sentences that only link two things the owner already said.
- Fixes: spelling, grammar, punctuation, capitalization, consistency.
- Scaffolding the project's post format requires.

What you may not add, even when it would make the piece "better":
- New examples, stories, numbers, stats, quotes, names, tools, engines, or dates.
- New opinions or a stronger or weaker version of the owner's opinion (no added hedging, no added certainty).
- Background, history, or "context" paragraphs the owner didn't write.
- A conclusion, lesson, or takeaway the owner didn't state or clearly imply.
- Facts you looked up. Research goes in the report as a suggestion, not into the post as the owner's words.

Models asked only to fix grammar still drift the meaning and neutralize the author's stance, and they tend to rewrite for fluency when a minimal edit was asked for (see [sources](references/sources.md)). So edit at the lowest level that fixes the problem, and keep the owner's distinctive phrasing word for word unless it's actually broken.

## It has to sound like a person wrote it

Faithful content isn't enough. If the piece reads like AI wrote it, readers will assume AI wrote it, and the owner loses the trust the post was meant to build. The finished piece should sound like the owner talking to a friend who builds things too: personal, warm, a little opinionated, sometimes rough. Never clinical, cold, corporate, or polished to the point of sounding like a press release.

- **Keep the owner's texture.** Their humor, asides, admissions ("my first ones were terrible"), and casual phrasing are the voice. Fix typos and broken grammar; don't iron out personality. "my first ones were terrible lol" can become "My first ones were terrible", not "My early work was a learning experience". If it sounds like them with the mess removed, it's right. If it sounds like a smoother stranger, it's wrong.
- **First person, plain words.** "I rewrote it twice" beats "The system underwent two iterations." Short sentences, contractions, varied rhythm. A fragment now and then is fine.
- **No em dashes** unless the voice guide allows them. Use commas, periods, or parentheses. Em dashes are one of the first things readers point to as an AI tell. Search your output for "—" before handing it back.
- **No AI tells.** See [AI tells](references/ai-tells.md) and strip every one. When the owner's raw notes are blunt, keep them blunt.
- **Read it aloud in your head.** For every paragraph ask: would the owner actually say this, out loud, in these words? If a line sounds like a chatbot, a marketing page, or a textbook, rewrite it closer to their original notes.

When there's tension between "polished" and "sounds like them", pick "sounds like them".

### Notes should become prose, not tidied bullets

Faithful isn't the same as finished. A common miss is keeping one sentence per line in the order the bullets came, which reads like cleaned-up notes rather than a post. The job is to make the owner's points flow the way they'd say them out loud.

- Join related points into real paragraphs of two to four sentences. Use the owner's own words, and connect them with small joining words ("so", "but", "and that's the thing", "which is why") only where the link between the two points is already in the notes. A joining word must not create a reason, cause, or conclusion the owner didn't give.
- Vary the rhythm: a longer sentence that carries the reasoning, then a short one that lands it. One-line paragraphs are for emphasis, not the default: one or two in a whole post. If most of your paragraphs are a single sentence or map one-to-one onto the owner's bullets, merge again.
- Short notes make a short post, and that's fine. Short isn't the problem; choppy is. A 250-word post in three real paragraphs reads better than the same words in nine fragments.
- Headings only where they help a reader navigate. An opinion or story post (the owner sharing a take, a frustration, a lesson) gets no headings by default: it runs as one piece, joined by spoken transitions built from the owner's lines ("And PRs are where I notice it most"), with at most one `---` before the closing thought. Headings belong in posts a reader jumps around in: tutorials, comparisons, reference lists, long build stories, postmortems. A heading every couple of paragraphs makes a blog post read like a website with sections, and each one resets the voice. Never put a heading over a single short paragraph, and don't add headings to a draft the owner already wrote as flowing prose.
- When a heading earns its place, write it in sentence case and label what the section actually holds, so a reader skimming knows what's there. "How I fixed it with skills" says something; "How I push it to do better" doesn't.
- Keep each point next to the point it supports. Reorder to improve flow, but don't move a line away from the idea the owner tied it to (a story about scale belongs beside the lesson it illustrates, not in the intro).

Here's the difference, using notes that say "the feel of a game is the whole thing. you cant prompt your way to a jump that feels good. you have to play it 100 times and tweak" and "been making games since flash. my first ones were terrible lol":

```md
❌ Faithful but notes-like:
The feel of a game is the whole thing.

You can't prompt your way to a jump that feels good. You have to play it 100 times and tweak.

I've been making games since Flash. My first ones were terrible.

✅ Faithful and readable:
The feel of a game is the whole thing. You can't prompt your way to a jump that feels good. You have to
play it 100 times and tweak. I've been making games since Flash, and trust me, my first ones were terrible.
```

The ✅ version adds no claim. It only joins sentences and keeps the owner's "lol" as a spoken "trust me". If you're unsure whether a joining phrase adds meaning, leave it out.

## When something is missing: query, don't fill

Professional editors don't fill gaps. They ask the author. Do the same.

- Put a marker in the post only for gaps the post can't stand without: ones the owner flagged themselves ("need an example here"), or a missing piece that breaks the argument. Optional additions ("a story here would make this land harder") are questions in the report, not markers. A post with a TK after every paragraph reads like an outline and is harder for the owner to review; one or two markers is typical.
- In the draft, leave a visible marker where the gap is: `[TK: one line on what's needed]`. TK is the editor's standard "to come" mark, and it's easy to search for before publishing. Never hide it in an HTML comment, which would vanish from the rendered page and could ship unnoticed.
- In your report, ask a short numbered question for each gap. Offer options drawn from the owner's own material when you can ("Was it the jump or the wall slide?"), and ask openly when you can't. Don't suggest a made-up answer as an option.
- If the owner asks you to "make it longer" or "add examples/stats", the honest way to do that is questions. Ask what they'd add. Length comes from their answers, not your inventions.
- If the request is a topic with no material ("write a post about X"), don't draft. Ask for their raw thoughts: a few bullets, a voice memo transcript, anything. Offer two or three questions to get them started.

## The editor's report

Keep it short and scannable. Use this structure:

```md
## Editor's report

**Queries** (answer these and I'll fold them in)
1. [TK in "Section name"] The question.
2. ...

**Fact-check**
- "Claim as written": verified / looks off (why, with link) / couldn't verify.

**Suggested links** (optional, only if useful)
- Where it would go, and the URL.

**What I changed**
- Structure: one line on how it was organized.
- Line edits: the few changes that matter, quoted before → after.
- Cut: anything removed and why.

**Trace check**: every claim, number, and opinion in the post comes from your notes, except the TK markers above.
```

If you had to cut something you added during editing because it had no source, say so in "What I changed". That honesty is the point of the report.

## Titles and descriptions

The title is the owner's. Keep the one they gave. If they gave none or asked for options, suggest two or three in the report, built only from their own phrasing, and put your best guess in the post's metadata. The description should summarize only what the post says.

Never rename or change the slug, title, or metadata of a post that's already published without the owner's explicit approval: a changed slug breaks every link to it.
