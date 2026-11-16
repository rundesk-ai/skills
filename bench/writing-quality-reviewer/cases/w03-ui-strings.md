+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "easy"
fixture = "ui-strings"
cases_version = 1
key = """
must:
  M1 destructive  The delete dialog ("Are you sure?" / "This action cannot be undone." / "OK") does not name what will be lost (the project's files and deploy history) and the confirm button is "OK", not the act.
  M2 error  `errors.save` "An error has occurred." gives no cause or fix although the response carries field, reason and max.
  M3 term  "Archive Workspace" names the entity "workspace" where everything else says project.
  M4 button  `invite.button` "Submit" does not say it sends an email invitation.
  M5 slot  `settings.retries.label` names the mechanism ("How retries are handled") and its tooltip repeats the label ("Retries"); the tooltip should carry what the label cannot (retries of a failed deploy, 0 to 10).
  M6 plural  "{count} item(s) selected": no plural rules, and "item" for project.
decoys:
  D1 `projects.delete.cancel` "Cancel" is right; flagging it is a false positive.
taste:
  T1 key naming in strings.json; T2 ICU versus another plural syntax.
extras:
  X1 `projects.empty` is chatty ("Oops!", "awesome") with no clear action.
  X2 `projects.filtered_empty` gives no way to widen the filters.
  X3 `errors.name_taken` hedges ("It looks like... may") about a fact the API knows.
  X4 "Archive Workspace" is title case beside sentence-case strings.
"""
+++
Review the interface strings in strings.json before they ship. USAGE.md says how each one is used.
