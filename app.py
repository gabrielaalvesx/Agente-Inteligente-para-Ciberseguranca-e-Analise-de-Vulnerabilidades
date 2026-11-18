"""Exemplo corrigido: login local com consulta parametrizada.

Demonstra apenas a mitigação de SQL Injection. Não é um sistema de autenticação
pronto para produção (senhas fictícias em texto simples são usadas para isolar
o assunto do laboratório).
"""
import sqlite3


def create_database():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [("alice", "senha-demo-alice"), ("bob", "senha-demo-bob")],
    )
    return conn


def authenticate(conn, username, password):
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    return conn.execute(sql, (username, password)).fetchone()


def main():
    conn = create_database()
    print("Login legítimo:", authenticate(conn, "alice", "senha-demo-alice"))
    payload = "' OR '1'='1' -- "
    print("Tentativa com entrada de SQLi:", authenticate(conn, payload, "qualquer"))
    conn.close()


if __name__ == "__main__":
    main()
