# AGENTS

`uploads` stores and serves files that customers attach to support tickets. Node 20, ES modules, no
dependencies. Attachments include invoices and ID documents, and the server also holds its own
configuration and keys.

## Rules

- **Files are served only from `uploads/`.** A request must never read a file outside it.
- **A request body is capped at 10 MB.** Read no more than that before rejecting the request.

## Build, test & run

```sh
npm test
```
