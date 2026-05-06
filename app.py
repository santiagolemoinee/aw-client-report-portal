"""AW Client Report Portal — Flask application entry point.

Internal tool for Windbrook Solutions (EF) to generate quarterly
SACS (cashflow) and TCC (net worth) reports for high-net-worth clients.
"""
import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Root route — Phase 0 placeholder. Will redirect to /clients in Phase 2."""
    return jsonify(
        {
            "app": "AW Client Report Portal",
            "client": "Windbrook Solutions",
            "phase": "0 — Setup & Deploy",
            "status": "online",
        }
    )


@app.route("/health")
def health():
    """Health check endpoint for Railway monitoring."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
