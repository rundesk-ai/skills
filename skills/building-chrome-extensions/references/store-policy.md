# Store policy

The rules that actually get a listing rejected or removed. Violation notices arrive as a
colour-and-element pair — `Grey Titanium`, `Purple Potassium` — so each rule below names its code.

## Single purpose

> An extension must have a single purpose that is narrow and easy to understand. Don't create an
> extension that requires users to accept bundles of unrelated functionality.

A purpose may be a narrow **subject matter** (weather, maps) _or_ a narrow **browser function** (a
new tab page). Either way the extension must respect the user's other settings. Permissions are read
as evidence of purpose: _"We assume your extension utilizes each of the permissions it requests.
Excessive permissions unrelated to your extension's single purpose will be viewed as enabling
unrelated functionalities."_

Codes: `Red Magnesium`, `Red Copper`, `Red Lithium`, `Red Argon`.

## Repetitive content — the sharpest risk for a template or a family of listings

> We don't allow any developer, **related developer accounts, or their affiliates** to submit
> multiple extensions that provide duplicate experiences or functionality.

And explicitly: _"developers cannot submit content that provides the same user experience, even if
the metadata or code are not identical"_, plus a named violation for _"template extensions which
create a spammy experience"_. Locale variants of one product are called out as a violation.

**The saving clause is the one to build to:** _"Multiple extensions that provide different user
experiences are not considered repetitive content."_ A vertical that genuinely differs — different
widgets, different data, different audience — is the defence. Shared chrome around identical
behaviour is not.

Code: `Yellow Nickel`.

## Affiliate and monetization

The policy says three things:

> - Any affiliate program must be described prominently in the product's Chrome Web Store page,
>   user interface, **and before installation**.
> - Affiliate links, codes, or cookies must only be included when the extension provides a
>   **direct and transparent user benefit** related to the extension's core functionality.
> - **Related user action is required** before the inclusion of each affiliate code, link, or cookie.

**A URL carrying an identifier used to track conversions is an affiliate URL** by the store's own
definition, whatever it is attached to.

The enforcement page is narrower than the policy text, and lists only two triggers: use **without
proper disclosure in the description and the user interface**, and **no related user action**.

**Where this is genuinely untested — do not write code as though either reading is settled.** The
affiliate FAQ addresses shopping, coupons and cashback; it says nothing about search affiliate
parameters. Whether search results themselves satisfy the benefit test has no published answer, and
whether choosing a named provider from a menu counts as related user action is undecided.

**What follows from that:** disclosure is the demonstrably enforced dimension and is cheap — three
places, every time: the store listing, the extension's own interface, and before installation.

Code: `Grey Titanium`.

## Data handling

**Local storage still triggers every obligation.** The store is explicit: extensions must disclose
how they handle user data _"even when data is processed or stored locally on a user's device and is
not transmitted"_, and a privacy policy is required even then.

**The disclosure must be in the interface.** Not only in a privacy policy, and not only in the store
listing. Two official pages disagree on this — follow the stricter one.

**Limited Use requires:**

> Any user data collected by an extension must now be **strictly necessary to the extension's
> disclosed single purpose**. Collecting data for other purposes is prohibited.

All collection must be disclosed _"regardless of whether the data is closely related to the
extension's single purpose"_, and a later change in practice must be disclosed proactively. The FAQ
is blunt that _"ad targeting or other monetization of this data isn't for a user-facing feature"_.

**Read this against any activity beacon.** A persistent identifier and an advertising click id sent
on every new tab are hard to defend as strictly necessary to a weather page's single purpose.

Codes: `Purple Nickel`, `Purple Magnesium`, `Purple Lithium`.

## Permissions at review

`Purple Potassium` usually does **not** mean "too much". The two documented causes are that the
reviewer could not see the code using a permission, and **starter-template residue** — permissions
inherited from a scaffold and never called. Before submitting, grep for every declared permission
and delete the ones with no call site.

A justification that passes names three things: the user-visible feature, the data flow, and why a
narrower permission is insufficient. _"Needed to work with tabs"_ fails.

The reviewers apply the permission definitions literally. `activeTab` does **not** grant passive
access to the focused tab. `tabs` is **not** needed for `chrome.tabs.create`. `storage` is not
needed for Web Storage.

## Review and enforcement

Every submission is reviewed, updates included; there is no fast lane for tenure or install base,
and Chrome's developer relations have said plainly _"we don't have a process for expediting
reviews."_ Plan **two to four weeks** for a first submission and days for an update.

**A stuck review costs the fix, not the listing** — the published version stays up and installable
throughout.

The ladder runs rejection → warning (7–30 days to fix, listing stays live) → takedown (404, and
Chrome auto-disables it for users after several weeks) → malware removal, which disables it on every
device with no way for the user to re-enable.

**Recovery from a spam or malware classification is close to zero.** Unrelated extensions sharing
one monetization platform have been removed together, appeals answered _"Given the nature of this
violation the item will not be reinstated"_, and resubmissions with the monetization removed still
rejected. There is **one appeal per violation**.

## Shipping several extensions from one account

A partner host, suggestion endpoint, or activity beacon shared across listings means they **do not
fail independently**: with the spam policy's reach over _"related developer accounts, or their
affiliates"_, one adverse classification of the shared path can take every listing down at once.
Keep a partner integration per listing, behind that listing's own configuration.

## Account facts worth knowing

- **$5 once**, no renewal. Two-step verification is mandatory before publishing.
- **The account email is immutable**, and every rejection and takedown notice goes there. Use a
  monitored address.
- **New accounts are capped at two published extensions.** Request an increase from the dashboard
  before a third listing.
- There is **no store dormant-account policy**; the two-year rule people cite is general Google
  account inactivity.
