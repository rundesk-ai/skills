const SITE = new URL('https://shop.example');

// Where to send the user after sign-in: the `next` they asked for when it is a path on this
// site, otherwise the home page.
export function safeNext(next) {
  if (typeof next === 'string' && next.startsWith('/')) return next;
  return '/';
}

// For links that may be absolute: keep them only when they resolve to this site's origin.
export function sameSiteUrl(href) {
  try {
    const url = new URL(href, SITE);
    return url.origin === SITE.origin ? url.pathname + url.search : '/';
  } catch {
    return '/';
  }
}
