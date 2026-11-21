+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "terse-errors"
cases_version = 2
key = """
must:
  M1 raw-error  `errors.folder_missing` "folder not found: {path}" is a raw fragment, lower case, with no cause or next step, though USAGE.md gives both (moved, renamed or deleted; Choose folder on its row in the sidebar). The fix must keep {path}, name the `Choose folder` control exactly, stay brief, and may use a contraction; e.g. "Couldn't find {path}. It may have moved; choose Choose folder on its row in the sidebar."
  M2 consequence  `errors.session_unsaved` speaks about the system ("The database is not open", "is not kept") instead of what the person loses; the fix says in plain, human words that this session's history won't be there once it stops or they quit, keeping both conditions.
  M3 monotone  `help.snapshots` is five sentences that each open on "Tidepool"; reported as one cadence finding, with a fix that joins the facts (every hour, 30 days, then one a day for a year, stored on this Mac, so restores work offline) and keeps all of them.
  M4 wrong-condition  `errors.sync_paused_metered` says "waits for Wi-Fi" where USAGE.md says an unmetered network (an unplanted defect the first run found; the key was corrected after it).
decoys (flagging is a false positive):
  D1 Removing the contractions or the natural tone of `errors.sync_paused_metered` while fixing M4.
  D2 Any proposed fix that is chatty ("Oops!", "Uh oh", "Don't worry"), drops {path}, or turns a sentence more formal ("The specified folder could not be located", "connectivity").
  D3 Any fix that drops a fact (one of the snapshot intervals, offline restore, the quit condition).
taste (neither):
  T1 the ellipsis in "Choose folder…" in USAGE.md; T2 key names.
extras:
  X1 noting that the error bar strings should end with a period; neutral.
"""
+++
Review the strings in strings.json before they ship. USAGE.md says where each appears and what the content guide asks.
