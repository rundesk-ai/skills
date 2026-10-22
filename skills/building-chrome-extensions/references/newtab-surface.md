# The new-tab surface

Read this when an extension overrides the new tab. It is the most heavily policed category in the
store.

## The search rule

The load-bearing policy for any new tab carrying a search box, quoted from Chrome's own quality
guidelines:

> **Can my New Tab Page (NTP) extension make changes to the user's web search experience? No.**
> NTP extensions that provide a web search experience must respect the user's existing web search
> settings by using the Chrome Search API.

A product may offer several providers, **as long as the top or default option is the one the user
already chose in their browser settings**. A _vertical_ search — over open tabs, or one named
platform — is allowed. A _horizontal_ web search is what the rule governs.

**`chrome.search.query()` takes `{ text, disposition, tabId }` and nothing else.** There is no
parameter for an affiliate identifier. The compliant path and the monetizable path are
architecturally disjoint, and no amount of configuration reconciles them.

## What the browser owns

- **Incognito cannot be overridden.** Chrome states plainly that extensions cannot override the new
  tab in incognito windows; incognito shows the built-in page while the extension keeps working in
  normal windows.
- **The address bar takes first focus.** Chrome's own guidance: _"Remember that new tabs give
  keyboard focus to the address bar first. Don't rely on keyboard focus defaulting to other parts
  of the page."_ Do not use `autofocus`, do not call `.focus()` on load, and do not add a global
  key handler to capture the first keystroke — those keystrokes go to the omnibox, the page never
  sees them, and succeeding would be the anti-pattern the guidance prohibits.
- **`chrome://newtab` is the extension's own page**, so it cannot be used as an escape hatch.
- **One override page per extension**, and it must be a bundled file.
- **Treat every open as a cold start.** Nothing documents prerendering of an extension new tab, so
  the whole framework boots on every new tab. Keep the first paint small.

## The flash

The most-reported complaint against new-tab extensions, and only partly fixable: the browser paints
a default canvas before the extension's first paint. In order of leverage:

1. `<meta name="color-scheme" content="dark light">` in `<head>` — lets the browser pick the right
   initial canvas before any CSS parses. The highest-value single line for a dark page.
2. Background colour on `html`, inline in a `<style>` in `<head>`. An external stylesheet is one
   round trip too late.
3. **Seed the theme from synchronous storage for the first paint and reconcile from
   `chrome.storage` afterwards.** Gating the first paint on an asynchronous read guarantees a
   wrong-theme flash.
4. No fade-in on the shell, and no webfont or hero image on the critical path.

## Policy for new-tab extensions

The category is named directly in the store's own examples:

- The single-purpose violation list names _"New Tab Page extensions that alter the user's web
  search experience and don't respect the user's existing search settings."_
- The definition of click-bait uses a new-tab extension as its worked example.
- **Changing the default search engine is a separate purpose** from replacing the new tab. The only
  compliant route is the settings-overrides API, and the domains used must be verified in Search
  Console by the publishing account.

Two official pages disagree on whether an override page may carry other functionality. The narrower
page says an override extension _"may not provide any other functionality"_; the policy FAQ allows
several functions within one narrow subject matter. **A vertical new tab — weather, with weather
widgets — is defensible under the FAQ. Adding general web search to it is what pushes toward two
purposes**, which is precisely why the search rule exists as the escape valve.

## Per-release regression checks

Chrome releases have changed new-tab override behavior without warning — incognito handling and
bookmarks-bar visibility among them. Check on every Chrome release, because nothing else will:

- The page still overrides, in a normal window.
- Incognito behaves as expected.
- The bookmarks bar stays hidden when the user has hidden it.
- First paint carries no flash in dark mode.

Watch the `chromium-extensions` group as well as the release notes; breakage often surfaces there
first.
