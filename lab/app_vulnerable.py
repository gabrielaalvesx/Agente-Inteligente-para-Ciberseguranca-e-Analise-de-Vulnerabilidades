"""EXEMPLO INTENCIONALMENTE VULNERÁVEL — somente laboratório local."""
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


def authenticate_vulnerable(conn, username, password):
    # NÃO use este padrão em aplicações reais.
    sql = (
        "SELECT id, username FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )
    print("Consulta montada:", sql)
    return conn.execute(sql).fetchone()


def main():
    conn = create_database()
    payload = "' OR '1'='1' -- "
    print("Tentativa controlada:", authenticate_vulnerable(conn, payload, "inválida"))
    conn.close()


if __name__ == "__main__":
    main()
