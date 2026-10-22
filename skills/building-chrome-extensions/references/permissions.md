# Permissions

## The two lists

Declare both lists in one place, and make that declaration the gate:

```js
permissions: {
  required: ['storage', 'search'],
  optional: ['topSites', 'favicon'],
}
```

`required` is the install prompt. `optional` is requested later, from a user gesture. Have the
build assert that each manifest's lists match that declaration exactly, so a permission cannot
enter through a manifest alone.

## What Chrome refuses in `optional_permissions`

Chrome fails the **whole manifest** for any of these, so the declaration gate refuses them at
the earliest possible point:

`debugger` · `declarativeNetRequest` · `devtools` · `geolocation` · `mdns` · `proxy` · `tts` ·
`ttsEngine` · `wallpaper`

The same names are perfectly valid in the **required** list. The restriction is about being
optional, not about the capability.

## Warnings, and how they absorb each other

The install dialog is not one line per permission. Chrome applies rules in precedence order, and a
rule that fires **consumes** the permissions below it:

```
full access (debugger)
  └ <all_urls>          absorbs specific hosts, tabs, topSites, favicon, webNavigation
      └ history         absorbs tabs, topSites, favicon, webNavigation
          └ tabs        "Read your browsing history"; absorbs topSites, favicon
              └ topSites, favicon    stand alone only if nothing above claimed them
```

The strings the user actually reads:

| Declaration                   | Warning                                                |
| ----------------------------- | ------------------------------------------------------ |
| `chrome_url_overrides.newtab` | "Replace the page you see when opening a new tab"      |
| `topSites`                    | "Read a list of your most frequently visited websites" |
| `favicon`                     | "Read the icons of the websites you visit"             |
| `tabs`                        | "Read your browsing history"                           |
| `<all_urls>`                  | "Read and change all your data on all websites"        |

**Two consequences for a new-tab extension with no host permissions.** First, the override itself is
a warning you cannot avoid or make optional. Second, nothing absorbs `topSites` and `favicon` — each
adds its own visible, alarming line. That is the real argument for keeping both optional, and it is
stronger than the `favicon`-specific reasoning alone.

Free of any warning, and worth reaching for: `activeTab`, `alarms`, `contextMenus`, `offscreen`,
`scripting`, `search`, `storage`, `unlimitedStorage`, `sidePanel`, `idle`. Note that `scripting` and
`cookies` are free only because the host permission beside them carries the warning — it moved, it
did not disappear.

> There is **no credible public data** linking permission warnings to install conversion. Every
> figure in circulation is uncited. The case for minimising permissions rests on policy, review
> time and update survival, which is strong enough on its own.

## Requesting

Request from the gesture, and handle the refusal:

```js
// Called directly from the click handler; the request is the first await.
async function enableSiteIcons() {
  const granted = await chrome.permissions.request({ permissions: ['favicon'] });
  if (!granted) return; // the packaged fallback stays; nothing claims otherwise
  showSiteIcons();
}
```

**The gesture requirement is enforced, not advisory.** Calling outside one throws
`This function must be called during a user gesture`. Two consequences:

- **A service worker cannot call `permissions.request()`** — there is no gesture there, and a
  gesture does not forward from a content script. Call from the page.
- **Never `await` anything before the request** inside a click handler. The first `await` consumes
  the gesture.

Chrome remembers consent: after `permissions.remove()`, requesting again usually re-grants **without
prompting**. A user may revoke host access at any time from the extensions page, so listen to
`permissions.onAdded` and `onRemoved` and handle revocation live.

## Why optional matters at update time

**Adding a warning-triggering permission in an update disables the extension** until every user
re-accepts it. Optional permissions avoid that entirely. Changing `host_permissions` or a content
script's `matches` triggers it too.

Before any release that touches `permissions`, `host_permissions`, `content_scripts.matches`,
`chrome_url_overrides` or `chrome_settings_overrides`: pack the extension, drag the package onto the
extensions page, and read the real dialog. The Extension Update Testing Tool shows the _update_
dialog specifically — that is the one that decides whether a release disables itself for existing
users.
