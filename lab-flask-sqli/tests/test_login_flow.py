import os
import tempfile
import unittest

import db  # noqa: F401

from db import get_connection, init_db  # noqa: E402
from app import app as fixed_app  # noqa: E402

# Entradas maliciosas usadas no plano de regressao (veja o README).
PAYLOADS = [
    "' OR '1'='1' -- ",
    "' OR 1=1 --",
    "admin' --",
    "' UNION SELECT 1, 'x', 'y' --",
    "1; DROP TABLE users; --",
]


class TestLoginFixed(unittest.TestCase):
    def setUp(self):
        # Cada teste usa seu proprio banco SQLite temporario, sem compartilhar
        # estado com os demais testes.
        fd, self._tmp_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.environ["LAB_DB_PATH"] = self._tmp_path
        db.DB_PATH = self._tmp_path

        init_db()
        fixed_app.config["TESTING"] = True
        self.client = fixed_app.test_client()
        self.client.post(
            "/register",
            json={"username": "alice", "password": "senha-demo-alice"},
        )

    def test_login_legitimo(self):
        resp = self.client.post(
            "/login",
            json={"username": "alice", "password": "senha-demo-alice"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["username"], "alice")

    def test_login_rejeita_payloads(self):
        for payload in PAYLOADS:
            with self.subTest(payload=payload):
                resp = self.client.post(
                    "/login",
                    json={"username": payload, "password": "qualquer"},
                )
                self.assertNotEqual(
                    resp.status_code, 200,
                    "payload nao deve autenticar: {}".format(payload),
                )

    def test_login_outro_usuario(self):
        self.client.post("/register", json={"username": "bob", "password": "bob123"})
        resp = self.client.post("/login", json={"username": "bob", "password": "bob123"})
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        # Limpeza segura do arquivo temporario do teste.
        if os.path.exists(self._tmp_path):
            os.unlink(self._tmp_path)
        db.DB_PATH = None


if __name__ == "__main__":
    unittest.main()
