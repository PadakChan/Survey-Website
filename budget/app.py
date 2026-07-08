"""Ledger — a small personal budget app with a Google Sheets backup.

Entries (expenses and income) are stored in SQLite (budget.db, next to
this file), along with two settings: a monthly budget and a starting
balance. The "Back up to Google Sheets" button pushes every entry to a
Google Apps Script web app, which rewrites the target sheet — see
README.md for setup.
"""

import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import date

from flask import Flask, Response, g, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "budget.db")
CONFIG_PATH = os.path.join(BASE_DIR, "sheet_config.json")

# The main site's static folder, for the shared handwriting font.
SITE_STATIC = os.path.join(os.path.dirname(BASE_DIR), "static")

app = Flask(__name__, static_folder=SITE_STATIC, static_url_path="/static")

EXPENSE_CATEGORIES = {"Food", "Transport", "Shopping", "Other"}
SETTING_KEYS = {"monthly_budget", "starting_balance"}

# When set (e.g. on the deployed server), every request needs this password.
# Left unset for local use, so nothing changes on your own machine.
PASSWORD = os.environ.get("LEDGER_PASSWORD", "")


@app.before_request
def require_password():
    if not PASSWORD:
        return None
    auth = request.authorization
    if auth and auth.password == PASSWORD:
        return None
    return Response(
        "This ledger is private. Sign in with any username and your password.",
        401,
        {"WWW-Authenticate": 'Basic realm="Ledger"'},
    )


# ---------------------------------------------------------------- database

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            tip REAL NOT NULL DEFAULT 0,
            memo TEXT NOT NULL DEFAULT ''
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value REAL NOT NULL
        )
        """
    )
    # Older databases predate income support; add the kind column if missing.
    cols = {r[1] for r in db.execute("PRAGMA table_info(entries)")}
    if "kind" not in cols:
        db.execute("ALTER TABLE entries ADD COLUMN kind TEXT NOT NULL DEFAULT 'expense'")
    db.commit()
    db.close()


init_db()


def entry_dict(row):
    return {
        "id": row["id"],
        "kind": row["kind"],
        "date": row["date"],
        "category": row["category"],
        "amount": row["amount"],
        "tip": row["tip"],
        "memo": row["memo"],
    }


def get_settings(db):
    values = {"monthly_budget": 0, "starting_balance": 0}
    for row in db.execute("SELECT key, value FROM settings"):
        if row["key"] in values:
            values[row["key"]] = row["value"]
    return values


# ------------------------------------------------------------------ pages

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# -------------------------------------------------------------------- api

@app.route("/api/data")
def data():
    db = get_db()
    rows = db.execute("SELECT * FROM entries ORDER BY date DESC, id DESC").fetchall()
    return jsonify({
        "entries": [entry_dict(r) for r in rows],
        "settings": get_settings(db),
    })


@app.route("/api/settings", methods=["POST"])
def save_settings():
    payload = request.get_json(silent=True) or {}
    db = get_db()
    for key in SETTING_KEYS & payload.keys():
        try:
            value = round(float(payload[key]), 2)
        except (TypeError, ValueError):
            return jsonify({"error": "Please enter a valid number."}), 400
        if value < 0:
            return jsonify({"error": "Please enter a valid number."}), 400
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
    db.commit()
    return jsonify(get_settings(db))


@app.route("/api/entries", methods=["POST"])
def add_entry():
    payload = request.get_json(silent=True) or {}

    kind = payload.get("kind", "expense")
    if kind not in ("expense", "income"):
        return jsonify({"error": "Invalid entry type."}), 400

    try:
        entry_date = str(payload.get("date", ""))
        date.fromisoformat(entry_date)
    except ValueError:
        return jsonify({"error": "That date doesn't look right."}), 400

    if kind == "income":
        category = "Income"
    else:
        category = payload.get("category")
        if category not in EXPENSE_CATEGORIES:
            return jsonify({"error": "Invalid category."}), 400

    try:
        amount = round(float(payload.get("amount")), 2)
        tip = 0 if kind == "income" else round(float(payload.get("tip") or 0), 2)
    except (TypeError, ValueError):
        return jsonify({"error": "That amount doesn't look right."}), 400
    if amount <= 0 or tip < 0:
        return jsonify({"error": "That amount doesn't look right."}), 400

    memo = str(payload.get("memo") or "").strip()[:80]

    db = get_db()
    cur = db.execute(
        "INSERT INTO entries (kind, date, category, amount, tip, memo) VALUES (?, ?, ?, ?, ?, ?)",
        (kind, entry_date, category, amount, tip, memo),
    )
    db.commit()
    row = db.execute("SELECT * FROM entries WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(entry_dict(row)), 201


@app.route("/api/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    db = get_db()
    cur = db.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "That entry is already gone."}), 404
    return jsonify({"ok": True})


# ------------------------------------------------------- google sheets sync

def sheet_webhook_url():
    """Apps Script web app URL, from $SHEET_WEBHOOK_URL or sheet_config.json."""
    url = os.environ.get("SHEET_WEBHOOK_URL", "").strip()
    if url:
        return url
    try:
        with open(CONFIG_PATH) as f:
            return str(json.load(f).get("webhook_url", "")).strip()
    except (OSError, ValueError):
        return ""


@app.route("/api/sync-sheet", methods=["POST"])
def sync_sheet():
    url = sheet_webhook_url()
    if not url.startswith("https://script.google.com/"):
        return jsonify({
            "error": "Google Sheets isn't connected yet. Follow budget/README.md "
                     "to put your Apps Script URL in sheet_config.json."
        }), 400

    db = get_db()
    rows = db.execute("SELECT * FROM entries ORDER BY date, id").fetchall()
    payload = {
        "entries": [
            {
                "id": r["id"],
                "kind": r["kind"],
                "date": r["date"],
                "category": r["category"],
                "amount": r["amount"],
                "tip": r["tip"],
                "total": round(r["amount"] + r["tip"], 2),
                "memo": r["memo"],
            }
            for r in rows
        ]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        return jsonify({"error": f"Couldn't reach Google Sheets: {e.reason}"}), 502

    # The Apps Script in README.md replies {"ok": true, "rows": N}.
    try:
        result = json.loads(body)
        assert result.get("ok")
    except (ValueError, AssertionError):
        return jsonify({
            "error": "Google Sheets sent an unexpected reply. In the Apps Script "
                     "deployment, make sure access is set to 'Anyone'."
        }), 502

    return jsonify({"ok": True, "count": len(payload["entries"])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8765)), debug=False)
