# AGENTS

`profiles` renders public member pages for a forum. Node 20, ES modules, no dependencies. Anyone
can register and choose a display name and a bio.

## Rules

- **Every user-supplied value is escaped with `escapeHtml` from `src/html.js`** before it goes into
  HTML.

## Build, test & run

```sh
npm test
```
