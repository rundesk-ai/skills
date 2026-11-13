from flask import Flask, jsonify

from .db import session
from .models import Invoice


def create_app():
    app = Flask(__name__)

    @app.get("/invoices/<int:invoice_id>")
    def show(invoice_id):
        invoice = session.get(Invoice, invoice_id)
        if invoice is None:
            return jsonify(error="not found"), 404
        return jsonify(id=invoice.id, total_cents=invoice.total_cents, status=invoice.status)

    @app.teardown_appcontext
    def remove_session(exc):
        session.remove()

    return app
