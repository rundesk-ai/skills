"""The server: one process on the home network, no accounts."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from pantry import store
from pantry.handlers import export, items

GET = {"/": items.list_items, "/low": items.low, "/export.csv": export.export_csv}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, kind, body):
        self.send_response(status)
        if status == 303:
            self.send_header("Location", body)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        handler = GET.get(self.path)
        if handler is None:
            return self._send(404, "text/plain", "not found")
        conn = store.connect()
        try:
            self._send(*handler(conn))
        finally:
            conn.close()

    def do_POST(self):
        if self.path != "/use":
            return self._send(404, "text/plain", "not found")
        length = int(self.headers.get("Content-Length", 0))
        form = {k: v[0] for k, v in parse_qs(self.rfile.read(length).decode("utf-8")).items()}
        conn = store.connect()
        try:
            self._send(*items.use(conn, form))
        finally:
            conn.close()


if __name__ == "__main__":
    connection = store.connect()
    store.migrate(connection)
    connection.close()
    HTTPServer(("0.0.0.0", 8765), Handler).serve_forever()
