---
name: building-chrome-extensions
description: Use when building, reviewing, or releasing a Chrome extension, including anything its manifest declares or the browser enforces — a manifest field, a required or optional permission, the service worker, a new-tab override, host access, storage limits, messaging, a store listing's single purpose, affiliate or data disclosure, Chrome Web Store review, or the Publish API. It supplies the Manifest V3 rules, the failure modes that never raise an error, and the gates that catch a violation before a listing does. Do not use for an ordinary website or PWA, or for the UI framework and styling inside an extension page.
---

# Build on the Chrome extension platform

## Consistency first

Manifest V3 allows several valid shapes, and the best choice is usually the one the project already
uses. Follow the established manifest layout, build, and permission pattern; introduce a second one
only to fix a defect, and say so.

## Adding a capability

1. **Read every manifest the build produces** before changing one. A development manifest and a
   release manifest that drift are two different extensions with one name.
2. **Decide whether the capability is required or optional.** Required is a permanent install prompt
   that every user reads before installing; optional is requested later, from a gesture.
3. **Declare it in one place, and generate or validate every manifest from that place.** A permission
   only the manifest knows about is a build failure waiting to become a review failure.
4. **Hold the manifests to an exact match** in the build, rather than by reading them side by side.
5. **Pack it and read the real install dialog** before any release that changes a permission or an
   override. That dialog is the only authority on what the user is actually shown.
6. **State the data flow in three places**: the extension's own interface, the privacy policy, and
   the store's privacy fields. A network call the listing does not disclose is a takedown, not a bug.

## Rule index

| Concern | Read |
| --- | --- |
| Manifest fields and the new-tab override | [manifest.md](references/manifest.md) |
| Required vs optional, warnings, and what Chrome refuses | [permissions.md](references/permissions.md) |
| Service worker lifetime, storage, alarms, messaging, remote code | [lifecycle-traps.md](references/lifecycle-traps.md) |
| Focus, the flash, incognito, and the search rule on a new tab | [newtab-surface.md](references/newtab-surface.md) |
| Single purpose, affiliate, disclosure, and review | [store-policy.md](references/store-policy.md) |
| Uploading and publishing from automation | [store-api.md](references/store-api.md) |

## Decision rules

- **A capability the default experience does not use is optional, or absent.** Every required
  permission is paid for by every user at the install prompt, whether or not they use the feature.
- **An optional permission is requested from the gesture that enables the feature** — the Save
  click, the toggle — never on load, never speculatively, and never after an `await` that would
  consume the gesture.
- **A denial leaves truthful UI.** The feature stays off, the control reflects that, and the
  fallback is the packaged one.
- **Nothing development-only reaches the packaged build.** Name the markers that mean "development"
  and have the build refuse them, rather than trusting that the right entry point was swapped.
- **One listing does one thing.** Anything reachable from the extension's own settings is read as
  part of its single purpose, so a feature that does not belong to that purpose does not belong in
  settings.
- **Nothing survives in the service worker.** Module-scope state is gone on the next wake, silently;
  read [lifecycle-traps.md](references/lifecycle-traps.md) before writing worker code.
- **A horizontal web search on a new tab routes through `chrome.search`,** which takes no affiliate
  identifier; read [newtab-surface.md](references/newtab-surface.md) before adding a search box.
- **An affiliate program is disclosed in three places** — the store listing, the extension's own
  interface, and before installation; read [store-policy.md](references/store-policy.md).
- **Never ship code or logic a server can change after review.** A remote configuration file is
  allowed; remotely hosted code is not, and remotely switched behavior is how malicious updates
  evade review.
