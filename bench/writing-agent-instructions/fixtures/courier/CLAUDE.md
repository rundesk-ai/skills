# AGENTS

**THIS FILE IS THE LAW FOR EVERY AI AGENT IN THIS REPOSITORY. READ ALL OF IT. EVERY TIME.**

Welcome to the service starter! This repository was created from the group's **service starter
template**. The template was first written in 2023 for the billing team and has since been adopted by
most service teams. This file explains how we work, how the code is laid out, and what great code
looks like here.

## About the team

We are a small team that cares deeply about **quality**, **craft** and **shipping**. We believe in
**clean code**, **strong typing** and **kindness in review**. Please write code you would be proud of.

## Project tour

- `src/server.js` is the entry point. It creates the HTTP server.
- `src/routes/` holds the route handlers. `src/routes/parcels.js` holds the parcel routes.
- `src/auth/` holds authentication and authorisation code.
- `src/money.js` holds money helpers.
- `src/log.js` holds logging helpers.
- `test/` holds the tests. There are currently **212 tests** in the suite and they all pass.
- `migrations/` holds the SQL migrations.
- `scripts/` holds scripts.
- `docs/` holds documentation. New joiners should start with `docs/setup/legacy-onboarding.md`.
- `package.json` is the package manifest.

## Ground rules

- **ALWAYS** write clean, readable, maintainable code. **NEVER** write messy code.
- **ALWAYS** follow best practices.
- **Every state-changing route is authorised by a Policy class in `src/policies/`.** **NEVER** check
  a role inline in a route. Create a Policy for each resource and call `policy.authorize(user, action)`.
- **Money is an integer in the currency's minor unit.** **NEVER** use a float for a fee. Add fees with
  `addFees` in `src/money.js`, which refuses a non-integer.
- **NEVER log a request body.** Bodies hold recipients' names and home addresses; `src/log.js` logs
  the method, path and status only. `yarn lint` fails on `console.log` in `src/`.
- **Migrations: ask first.** A migration that has run on staging is **NEVER** edited; add a new one.
- **Use `const` over `let`**, arrow functions for callbacks, and template literals over concatenation.
- **ALWAYS** use meaningful variable names.
- **Dependencies: ask first.** The service has none.
- **NEVER run `db:reset`.** `DATABASE_URL` points at the staging database the whole team and the
  customer's testers share; resetting it wipes their data. Use `db:migrate`.
- **NEVER put a real address in a fixture or a test.** Use an invented one.
- **Be kind in code review** and assume good intent.
- **ALWAYS** add tests for new behaviour. **A route without a test for its refusal is not finished.**
- **NEVER** commit directly to `main`. Open a pull request.
- **ALWAYS** keep functions short. A function longer than 30 lines **MUST** be split.

## Commands

```sh
yarn install      # install dependencies
yarn test         # run the 212 tests
yarn lint         # lint
yarn dev          # start the server
yarn db:migrate   # apply migrations
```

## Framework basics

Node's `http` module creates servers. A handler receives a request and returns a response. Use
`async`/`await` for asynchronous code rather than callbacks. ES modules use `import` and `export`.
Remember that `===` compares without coercion, and prefer it to `==`.

## Code gallery

The examples below show what good and bad code look like here. **Study them.**

### Naming

**BAD:**

```js
const d = getData();
```

**GOOD:**

```js
const parcels = listParcels();
```

### Comparison

**BAD:**

```js
if (role == 'admin') {}
```

**GOOD:**

```js
if (role === 'admin') {}
```

### Declarations

**BAD:**

```js
var total = 0;
```

**GOOD:**

```js
const total = 0;
```

### Callbacks

**BAD:**

```js
items.map(function (i) { return i.id; });
```

**GOOD:**

```js
items.map((i) => i.id);
```

### Strings

**BAD:**

```js
'Parcel ' + id + ' created'
```

**GOOD:**

```js
`Parcel ${id} created`
```

### Early return

**BAD:**

```js
if (ok) { doIt(); } else { return; }
```

**GOOD:**

```js
if (!ok) return;
doIt();
```

### Money

**BAD:**

```js
const fee = 4.5 + 0.5;
```

**GOOD:**

```js
const feeMinor = addFees(450, 50);
```

### Logging

**BAD:**

```js
console.log(req.body);
```

**GOOD:**

```js
logRequest(req, status);
```

### Authorisation

**BAD:**

```js
if (req.user.role !== 'dispatcher') return forbidden();
```

**GOOD:**

```js
new ParcelPolicy().authorize(req.user, 'create');
```

### Async

**BAD:**

```js
fetchParcel(id, function (err, p) {});
```

**GOOD:**

```js
const parcel = await fetchParcel(id);
```

### Defaults

**BAD:**

```js
const s = body.surcharge || 0;
```

**GOOD:**

```js
const { surchargeMinor = 0 } = body;
```

### Errors

**BAD:**

```js
throw 'bad fee';
```

**GOOD:**

```js
throw new TypeError('fee must be an integer minor unit');
```

### Loops

**BAD:**

```js
for (var i = 0; i < a.length; i++) {}
```

**GOOD:**

```js
for (const item of a) {}
```

### Status codes

**BAD:**

```js
return { status: 200, body: 'forbidden' };
```

**GOOD:**

```js
return { status: 403, body: 'forbidden' };
```

### Destructuring

**BAD:**

```js
const a = req.body.recipientAddress;
```

**GOOD:**

```js
const { recipientAddress } = req.body;
```

### Tests

**BAD:**

```js
test('works', () => {});
```

**GOOD:**

```js
test('a courier may not create a parcel', () => {});
```

## Git

Write commit messages in the imperative mood. Keep the subject under 72 characters. Explain **why**
in the body. Rebase before you open a pull request.

## Done means

- The code is **clean** and you are **proud** of it.
- `yarn test` passes (all **212** tests).
- `yarn lint` passes.
- You have double-checked everything.
