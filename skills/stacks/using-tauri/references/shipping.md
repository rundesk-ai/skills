# Shipping

Read this when a feature depends on the platform's webview, when adding a sidecar or bundled
resource, or when building, signing, updating or targeting mobile.

## Three webviews, not one browser

| Platform | Engine | Version |
|---|---|---|
| Windows | WebView2 (Chromium) | updates itself, separately from the app |
| macOS, iOS | WKWebView (Safari's WebKit) | tied to the OS version the user runs |
| Linux | WebKitGTK | whatever the distribution ships, often well behind Safari |

A web feature that works in your development browser and on one platform can be missing on
another. Check each API the frontend depends on against the oldest Safari and WebKitGTK you
support, and run the app on each target before release. Blank windows on Linux with some GPU
drivers have known workarounds (`WEBKIT_DISABLE_DMABUF_RENDERER=1`, and
`__NV_DISABLE_EXPLICIT_SYNC=1` on NVIDIA); set them in a launcher, not in code that every platform
runs. The development server (`devUrl`) is a different origin from the packaged app
(`tauri://localhost`, or `http://tauri.localhost` on Windows), so storage and CORS behaviour seen
in development do not carry over.

## Memory

Measure the webview's processes too: on macOS the starter app's own process used 29 MB of an idle
76 MB, the rest in WebKit's content, GPU and network processes, which are not its children.

## Sidecars and resources

- **A sidecar's file name carries the target triple:** `binaries/helper` in `bundle.externalBin`
  means a file `binaries/helper-aarch64-apple-darwin` on disk (`rustc --print host-tuple`). Without
  it the build fails with `resource path ... doesn't exist`; build one per target in CI. The bundle
  installs it without the suffix.
- From Rust, `app.shell().sidecar("helper")` takes the file name only; from JavaScript,
  `Command.sidecar('binaries/helper')` takes the `externalBin` string. Running it needs a
  `shell:allow-execute` (or `allow-spawn`) permission with `"sidecar": true` and the arguments the
  page may pass; never pass page input through unchecked.
- Bundled files resolve through `app.path().resource_dir()` (or `BaseDirectory::Resource`), never a
  path relative to the working directory, which differs between `tauri dev`, the bundle and each
  OS.

## Signing and notarization

- **macOS** outside the App Store needs a Developer ID certificate and notarization, or Gatekeeper
  blocks the download. Tauri signs during `tauri build` when `APPLE_SIGNING_IDENTITY` (or
  `APPLE_CERTIFICATE` and its password) is set, and notarizes with the App Store Connect API key or
  Apple ID variables. Without them the build is only ad-hoc signed and still succeeds. Check the
  result: `codesign --verify --deep --strict <app>`, `spctl -a -vv <app>`, and `xcrun stapler
  validate` on the `.dmg`. Removing the quarantine attribute by hand only hides the problem on your
  machine.
- **Windows** needs Authenticode signing for SmartScreen; configure it in `bundle.windows`.

## The updater

- The updater refuses any update not signed by the key whose public half is in
  `plugins.updater.pubkey`. **A lost private key means installed copies can never update again**;
  store it, and its password, outside the repository with a backup.
- `bundle.createUpdaterArtifacts: true` requires a `plugins.updater` section (`plugins > updater
  doesn't exist` otherwise). The build reads the key from `TAURI_SIGNING_PRIVATE_KEY` (the key
  itself, or an absolute path — a relative path failed with `Invalid symbol 46`) and its password
  from `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`. `.env` files are not read. A missing key fails the
  build only after the whole bundle is made: set it before the first release build in CI.
- The update manifest's `signature` field is the content of the `.sig` file, not its path or URL. A
  static `latest.json` is validated across every platform entry, so one malformed entry stops
  updates on every platform.
- Never set `dangerousInsecureTransportProtocol`: the signature guards the artifact, HTTPS guards
  which version is offered.
- The app needs `updater:default` in a capability to check from the page. On Windows the app exits
  when the installer starts, so code after `downloadAndInstall` never runs; put cleanup in the
  updater's `on_before_exit`. Elsewhere, restart with the process plugin's `relaunch`, which needs
  its own permission.

## Single instance and deep links

Register the single-instance plugin first, before other plugins. On Windows and Linux a deep link
starts a second process with the URL as an argument; only single-instance with its `deep-link`
feature hands it to the running app.

## Mobile

`tauri android init` and `tauri ios init` generate `src-tauri/gen/android` and `gen/apple`; they need
the Android SDK and NDK (`ANDROID_HOME`, `NDK_HOME`) or Xcode, and fail without changing the project
when those are missing. The shared code must live in `lib.rs` behind
`#[cfg_attr(mobile, tauri::mobile_entry_point)]`. Desktop-only plugins and APIs (sidecars, window
management, the updater) do not exist on mobile: gate them with `#[cfg(desktop)]` and limit their
capabilities with `"platforms"`.
