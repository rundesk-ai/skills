from pantry import render, store


def list_items(conn):
    page = render.render("list.html", title="Pantry")
    return 200, "text/html", page.replace("<!-- rows -->", render.rows(store.all_items(conn)))


def low(conn):
    page = render.render("list.html", title="Running low")
    return 200, "text/html", page.replace("<!-- rows -->", render.rows(store.running_low(conn)))


def use(conn, form):
    try:
        store.use(conn, int(form["id"]), int(form["amount"]))
    except (KeyError, ValueError) as exc:
        return 400, "text/plain", f"cannot use that: {exc}"  
    return 303, "text/plain", "/"
