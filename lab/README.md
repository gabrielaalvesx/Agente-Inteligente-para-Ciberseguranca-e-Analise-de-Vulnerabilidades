# Laboratório de SQL Injection

Execute a partir da raiz do repositório:

```bash
python lab/app_vulnerable.py
python app.py
```

- `app_vulnerable.py` concatena a entrada na consulta SQL e demonstra a falha em SQLite `:memory:`.
- `app.py` é a versão corrigida, com placeholders `?` e parâmetros vinculados.

O banco é temporário, contém somente usuários fictícios e não abre portas de rede. Não exponha nem adapte o exemplo vulnerável para um serviço público.

O exemplo usa senhas fictícias em texto simples apenas para isolar SQL Injection. Em produção, use Argon2id, scrypt ou bcrypt, além de TLS, rate limiting, gestão de sessão e privilégio mínimo.
