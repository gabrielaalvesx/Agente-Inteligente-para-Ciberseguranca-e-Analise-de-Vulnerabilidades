import os
import sqlite3

# Caminho do banco. Por padrao usa lab.db na pasta atual; em testes,
# o ambiente LAB_DB_PATH recebe um arquivo temporario.
DB_PATH = os.environ.get("LAB_DB_PATH", "lab.db")


def get_connection():
    """Abre uma conexao com o SQLite, retornando linhas como dicionarios."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria a tabela users se ela nao existir ainda."""
    conn = get_connection()
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "username TEXT NOT NULL UNIQUE,"
            "password TEXT NOT NULL)"
        )
        conn.commit()
    finally:
        conn.close()
