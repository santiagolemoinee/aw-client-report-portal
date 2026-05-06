"""AW Client Report Portal — Flask application entry point."""
import os
from flask import Flask, jsonify
from database import init_db, get_connection
from seed import seed_smith_family

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response


def startup():
    init_db()
    seed_smith_family()


@app.route("/")
def index():
    return jsonify({
        "app": "AW Client Report Portal",
        "client": "Windbrook Solutions",
        "phase": "1 — DB & Seed",
        "status": "online",
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/clients")
def list_clients():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, type, status, created_at FROM clients ORDER BY name"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/clients/<int:client_id>")
def get_client(client_id):
    with get_connection() as conn:
        client = conn.execute(
            "SELECT id, name, type, status, created_at FROM clients WHERE id = ?",
            (client_id,),
        ).fetchone()
        if not client:
            return jsonify({"error": "Client not found"}), 404

        persons = conn.execute(
            "SELECT first_name, last_name, dob, role FROM client_persons "
            "WHERE client_id = ? ORDER BY role",
            (client_id,),
        ).fetchall()

        static = conn.execute(
            "SELECT monthly_salary_client_1, monthly_salary_client_2, "
            "monthly_expense_budget, deductible_auto, deductible_home, deductible_health "
            "FROM client_static_financials WHERE client_id = ?",
            (client_id,),
        ).fetchone()

        trust = conn.execute(
            "SELECT name, property_address, last_zestimate, last_zestimate_date "
            "FROM client_trust WHERE client_id = ?",
            (client_id,),
        ).fetchone()

    return jsonify({
        "client": dict(client),
        "persons": [dict(p) for p in persons],
        "static_financials": dict(static) if static else None,
        "trust": dict(trust) if trust else None,
    })


with app.app_context():
    startup()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
