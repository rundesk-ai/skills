# How the strings are used

- `board.delete.body`: {name} is the Board name. "3 lists" is hard-coded, but a Board has any number of lists; the API returns `list_count`.
- `board.rename.help`: the API rejects names longer than 64 characters.
- `board.archived.toast` is shown beside a separate Undo link that restores the Board.
