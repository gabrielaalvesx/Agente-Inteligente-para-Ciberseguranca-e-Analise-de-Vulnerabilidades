from flask import Flask, jsonify, request

import db
import sqlite3

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return jsonify({"error": "username e password sao obrigatorios"}), 400

    conn = db.get_connection()
    try:
        # VULNERAVEL: concatena a entrada na string SQL.
        sql = (
            "INSERT INTO users (username, password) VALUES ('"
            + username
            + "', '"
            + password
            + "')"
        )
        conn.execute(sql)
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "usuario ja cadastrado"}), 409
    finally:
        conn.close()

    return jsonify({"ok": True}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    conn = db.get_connection()
    try:
        # VULNERAVEL: concatena a entrada na string SQL.
        sql = (
            "SELECT id, username FROM users "
            "WHERE username = '" + username + "' AND password = '" + password + "'"
        )
        row = conn.execute(sql).fetchone()
    finally:
        conn.close()

    if row is None:
        return jsonify({"error": "credenciais invalidas"}), 401

    return jsonify({"id": row["id"], "username": row["username"]}), 200


if __name__ == "__main__":
    db.init_db()
    app.run(host="127.0.0.1", port=5000)
