# The Publish API

Read this before automating uploads or publishing to the Chrome Web Store.

## Use v2

**Publish API v2 is the only supported version;** v1.1 is retired. Code, workflow templates, and
tools that still use the v1.1 shape fail. The differences are not cosmetic:

| Change            | v1.1 → v2                                                                                    |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Upload verb       | `PUT` → **`POST`**                                                                           |
| Path              | `/upload/chromewebstore/v1.1/items/{ext}` → `/upload/v2/publishers/{pub}/items/{ext}:upload` |
| Publisher id      | not used → **required in every path**                                                        |
| Cancel a review   | not possible → `:cancelSubmission`                                                           |
| Create an item    | possible → **removed**                                                                       |
| Change visibility | possible → **removed**                                                                       |

The publisher id is the developer-account id from Publisher settings, **not** the extension id.
A wrong one surfaces as `ITEM_NOT_FOUND`, which reads like a bad extension id and is not — the v2
path couples the two.

## What it cannot do

The API uploads and publishes a package. It cannot touch listing metadata of any kind: no
description, screenshots, category, **permission justifications, single-purpose text or privacy
declarations**.

Every listing's justifications and privacy declarations are therefore typed into the dashboard by
hand. Keep the canonical text for each listing in the repository so that dashboard entry is
transcription rather than improvisation.

Two preconditions must be met manually before automation can ever run for a listing:

1. The Store listing and Privacy tabs are filled in.
2. The item has been **published manually at least once** at its current visibility.

## Credentials

**Use a service account.** It is v2-only, one per publisher, and it removes three separate traps at
once. Enable the API, create the service account, and add its email in the dashboard under account
settings.

The traps it removes, if you use a refresh token instead:

- **The seven-day trap.** A consent screen left in _Testing_ issues refresh tokens that expire in
  seven days. Continuous integration then fails with `invalid_grant` exactly a week after it was
  set up, with no notification. Set the consent screen to _In production_.
- **Six months idle** expires a token.
- **One hundred refresh tokens per account per client**, after which creating one silently
  invalidates the oldest.

Verification is not required — the store's API scopes are neither sensitive nor restricted, and
Google states it may deliberately not verify an app holding the write scope.

## Treat the credential as a signing key

A leaked store credential has been used to publish a malicious update of a popular extension, and
**it passed review**. Store credentials are publisher-wide: they can publish any extension on the
account.

- Scope them to a protected environment with required reviewers.
- Pin third-party actions by commit.
- **Split upload from publish**, so automation only ever stages and a person releases.

## Errors worth matching

| String                                                 | What it actually means                                            |
| ------------------------------------------------------ | ----------------------------------------------------------------- |
| `Publish condition not met: ` (empty reason, HTTP 400) | The item is already in review. In v2, cancel the submission first |
| `ITEM_NOT_FOUND`                                       | Wrong extension id — or, in v2, a mismatched publisher id         |
| `invalid_grant`                                        | The seven-day trap, the six-month idle rule, or token eviction    |
| `IN_PROGRESS`                                          | Normal. Uploads are asynchronous; poll the status endpoint        |

The manifest version must increment on every upload. No rate limits are published; back off on 429.

## Tooling

`chrome-webstore-upload` 6+ and `chrome-webstore-upload-cli` 4+ speak v2 and require a publisher id;
version 3 of the CLI is v1-only. A workflow that sends no publisher id is still on the v1 shape and
must be migrated.
