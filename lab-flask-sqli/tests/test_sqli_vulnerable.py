"""
Teste separado: demonstra SQL Injection na versao vulneravel do laboratorio.

Arquivo: lab-flask-sqli/tests/test_sqli_vulnerable.py

O que ele faz:
- Cria um banco SQLite TEMPORARIO apontado pela variavel de ambiente
  LAB_DB_PATH (dados ficticios, sem contato com redes ou servidores).
- Inicializa a aplicacao dann versao vulneravel (scenario/vulnerable/app.py)
  usando o Flask test_client() (sem abrir portas).
- Mostra que uma entrada maliciosa (' OR '1'='1' -- ) consegue contornar a
  autenticacao na versao vulneravel (status 200, usuario retornado).
- Compara com a aplicacao corrigida (app.py), que rejeita o mesmo payload
  com status 401.

Nao altera tests/test_login_flow.py nem a aplicacao corrigida.
"""

import os
import sys
import tempfile
import unittest

# 3) Garante que os imports abaixo encontrem a raiz do projeto.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import db  # noqa: E401
from db import get_connection, init_db  # noqa: E401

# 4) A partir daqui, os modulos usam o banco temporario.
import scenario.vulnerable.app as vulnerable_app  # noqa: E402
from app import app as fixed_app  # noqa: E402

# Entradas maliciosas usadas no laboratorio (todas com dados ficticios).
PAYLOADS = [
    "' OR '1'='1' -- ",
    "' OR 1=1 --",
    "admin' --",
    "' UNION SELECT 1, 'x', 'y' --",
    "1; DROP TABLE users; --",
]


class TestSQLIVulnerable(unittest.TestCase):
    """Conjunto de testes para a aplicacao vulneravel."""

    def setUp(self):
        # Cada teste cria seu proprio banco SQLite temporario, sem compartilhar
        # estado com os demais testes.
        fd, self._tmp_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.environ["LAB_DB_PATH"] = self._tmp_path
        db.DB_PATH = self._tmp_path

        init_db()
        self.client = vulnerable_app.app.test_client()
        self.client.post(
            "/register",
            json={"username": "alice", "password": "senha-demo-alice"},
        )
        # Payload usado no laboratorio para tentar quebrar a autenticacao.
        self.payload = "' OR '1'='1' -- "

    def test_login_com_payload_contorna_autenticacao(self):
        """Demonstracao: a entrada maliciosa autentica SEM senha valida."""
        resposta = self.client.post(
            "/login",
            json={"username": self.payload, "password": "qualquer"},
        )
        # Versao VULNERAVEL: autenticacao contornada (200) mesmo com senha
        # invalida, pois a entrada foi injetada diretamente no SQL.
        self.assertEqual(
            resposta.status_code,
            200,
            "esperado bypass na versao vulneravel: {}".format(resposta.get_json()),
        )
        dados = resposta.get_json()
        self.assertEqual(dados.get("username"), "alice")

    def test_login_legitimo_continua_funcionando(self):
        """O fluxo legitimo ainda funciona na aplicacao vulneravel."""
        resposta = self.client.post(
            "/login",
            json={"username": "alice", "password": "senha-demo-alice"},
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["username"], "alice")

    def test_comparacao_correcao_rejeita_mesmo_payload(self):
        """Compara com a versao corrigida: o mesmo payload e rejeitado."""
        # fixed_app e a aplicacao Flask. Para requisitar rotas e obter
        # respostas (status, headers, corpo), eh preciso de um client de teste.
        fixed_client = fixed_app.test_client()
        resposta = fixed_client.post(
            "/login",
            json={"username": self.payload, "password": "qualquer"},
        )
        # Versao CORRIGIDA: o payload e tratado como dado e rejeitado.
        self.assertEqual(resposta.status_code, 401)

    def tearDown(self):
        # Limpeza segura do arquivo temporario do teste.
        if os.path.exists(self._tmp_path):
            os.unlink(self._tmp_path)
        db.DB_PATH = None


if __name__ == "__main__":
    unittest.main()
