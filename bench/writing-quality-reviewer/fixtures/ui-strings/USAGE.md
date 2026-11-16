# How the strings are used

- "workspace" and "project" are the same entity. The API and the rest of the interface call it a project.
- Deleting a project removes its files and all deploy history permanently.
- `errors.save` is shown when saving a project fails. The response carries `{field, reason}`, for example `{field: "name", reason: "too_long", max: 64}`.
- `errors.name_taken` is shown when the API returns 409 for a project name that already exists.
- `invite.button` sends an email invitation to the address typed in the form.
- The filter bar filters projects by status and owner; `projects.filtered_empty` shows when the filters match nothing.
- `settings.retries` sets how many times a failed deploy is retried before it is marked failed (0 to 10).
