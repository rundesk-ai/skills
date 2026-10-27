# AGENTS

Rules for every agent working in this repository. Shop is a Laravel 13 application where customers
place and cancel orders and download their order history; admins manage orders. Customers are billed
from what these pages and emails show, so a total, a status or a permission shown in one place must
match every other. Where this file conflicts with your general habits, this file wins.

## Before you work

Load light; pull depth only when the task needs it.

1. **Load every skill the work calls for — all of them, in one pass, before anything else.** An
   agent that has started editing has stopped loading. After a compaction, load them again.

   | The work | Load |
   |---|---|
   | Any PHP, Blade, route, migration or test in this application | `using-laravel` |

   The table is the floor, not the list. A skill changes *how* you work; it never widens scope or
   overrides this file.
2. **Read the code map below**, then the files the task enters.
3. **Read a file before editing it; search before writing new logic** — reuse or extend what is
   already here rather than duplicating it. Scratch files stay outside the repository.
4. **Make the smallest complete change.** First list every place it must reach: routes, controllers,
   views, translations, mail, tests. Then take the first option that fully works: does it need to
   exist; is it already here; does Laravel do it; otherwise the least new code that reads at a
   glance. Add no abstraction, wrapper, option, config or "for later" code nobody asked for; keep the
   structure the code already has, and prefer deleting to adding. Touch nothing the task did not send
   you to — improvements are mentioned, not made. Be lazy about the solution, never about the change:
   finish every caller, test and doc it breaks, and delete the code, tests, assets and config it
   leaves unused; list anything already unused for the owner, since it may be kept on purpose. Never
   cut authorization, validation or a migration — and code you move or merge keeps its own.
5. **Do not contradict the owner without evidence.** Investigate, then answer with what you found.

## Hard rules

The first three need explicit approval. The rest are not negotiable.

- **Dependencies — ask first.** Adding, removing, or version-bumping a Composer or npm package.
- **Deletions — ask first.** Any file outside the task's immediate scope.
- **Commits — ask first.** Never commit or push unless told to.
- **Never delete or edit a migration that has run.** Every fresh database is built from them. Add a
  new migration instead.
- **Never ship a page or email without its authorization.** Every order a user sees or changes is
  theirs, or they are an admin.

## Code map

| Path | Owns |
|---|---|
| `app/Models` | orders and users, and the rules about them |
| `app/Policies`, `app/Providers/AppServiceProvider.php` | who may do what |
| `app/Http` | controllers and form requests |
| `resources/views`, `lang/en` | pages, emails and their wording |
| `config/billing.php` | billing figures |
| `tests/Feature` | the application's behaviour |

## Build, test & run

```sh
php artisan test   # the suite; must pass
```

**Who runs the app:** run the tests to prove it works, then hand off — the owner runs the site and
judges it.

## Definition of done

Re-read this file and check each item below before calling the work done.

1. `php artisan test` passes — observed, not inferred.
2. Every rule here held.
3. New guaranteed behaviour is proven by a test seen failing without it.
4. The hand-off names what changed, what was deliberately left, and anything unused you noticed.
