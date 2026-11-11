"""Title to slug, and the checks around it."""
import re

MAX_LEN = 80
_NOT_ALLOWED = re.compile(r"[^a-z0-9]+")


def slugify(title):
    """Lowercase ASCII words joined by single hyphens, at most MAX_LEN long, cut at a word."""
    tmp = title.strip().lower()
    tmp = tmp.encode("ascii", "ignore").decode("ascii")
    tmp = _NOT_ALLOWED.sub("-", tmp).strip("-")
    if len(tmp) <= MAX_LEN:
        return tmp
    else:
        # Cut at the last hyphen that fits, so a slug never ends in half a word.
        cut = tmp[:MAX_LEN + 1].rfind("-")
        if cut <= 0:
            # One word longer than the limit: there is no word boundary to cut at.
            return tmp[:MAX_LEN]
        return tmp[:cut]


def is_slug(text):
    """True for text that slugify would return unchanged."""
    if not text or len(text) > MAX_LEN:
        return False
    tmp = text.strip().lower()
    if tmp != text:
        return False
    return _NOT_ALLOWED.sub("-", text).strip("-") == text


def unique_slug(title, taken):
    """A slug for `title` that is not in `taken`: the plain slug, or the slug with -2, -3, ... added."""
    base = slugify(title)
    if not base:
        raise ValueError("title %r has no ASCII letters or digits to make a slug from" % (title,))
    if base not in taken:
        return base
    n = 2
    while True:
        suffix = "-" + str(n)
        # Keep the whole thing within the limit by shortening the base, never the number.
        candidate = base[:MAX_LEN - len(suffix)].rstrip("-") + suffix
        if candidate not in taken:
            return candidate
        n += 1
