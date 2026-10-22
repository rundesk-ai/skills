# Manifest

When the build produces more than one manifest — a development one and a release one — generate or
validate both from one declaration. A committed `version` the build overwrites is not the one that
ships; check the packaged manifest.

## Fields to pin, and to validate in the build

| Field | Value |
| --- | --- |
| `manifest_version` | `3` |
| `version` | one source of truth, written at build time |
| `chrome_url_overrides.newtab` | a bundled HTML file, when the extension overrides the new tab |
| `background.service_worker` | the bundled worker file |
| `icons` | 16, 32, 48 and 128, all present on disk |
| `permissions` | exactly the declared required set |
| `optional_permissions` | exactly the declared optional set |

## Fields that must stay absent unless they are the purpose

- **`chrome_settings_overrides`.** A new-tab extension that also changes the default search engine
  has two purposes; see [newtab-surface.md](newtab-surface.md).
- **Host permissions the product does not call.** A host in the manifest is a prompt the user
  reads; it comes from a real request in the code or it does not appear.

## Version

The store requires the version to increase on every upload. Make a version bump its own reviewed
change rather than a side effect of a production build.
