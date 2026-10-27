# AGENTS

`auth` handles sign-up, sign-in, sessions and account settings for a shop at `shop.example`. Node
20, ES modules, no dependencies. It is the only thing between the internet and customer accounts.

## Rules

- **After sign-in, redirect only to paths on this site.**
- **Every request input is untrusted** until it has been checked here.
- **A session token expires 24 hours after sign-in.** `sign` sets `exp`; a token past it is refused.

## Build, test & run

```sh
npm test
```
