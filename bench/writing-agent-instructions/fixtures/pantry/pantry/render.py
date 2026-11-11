"""Fill a template. Every value is HTML-escaped here, so a template never escapes anything itself."""
import html
import os

TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def render(name, **values):
    with open(os.path.join(TEMPLATES, name), encoding="utf-8") as f:
        text = f.read()
    for key, value in values.items():
        text = text.replace("{{ " + key + " }}", html.escape(str(value)))
    return text


def rows(items):
    """Table rows for a list of items; names are escaped because the family types them."""
    return "".join(
        f"<tr><td>{html.escape(i['name'])}</td><td>{i['quantity']} {html.escape(i['unit'])}</td></tr>"
        for i in items)
