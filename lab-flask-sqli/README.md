# Laboratorio: API Flask com SQLite para analise de SQL Injection

## Escopo
- Ambiente: Ubuntu lab, rede isolada (host-only/NAT controlado), sem expoitura
  a internet.
- Aplicacao: API Flask pequena com login e cadastro.
- Banco: SQLite, sem servidor dedicado.
- Objetivo: reproduzir e corrigir SQL Injection, validar mitigacao e rodar
  testes de regressao.

## Como rodar
1. Instale as dependencias:
   pip install -r requirements.txt
2. Inicie a aplicacao correta (a do laboratorio, sem vulnerabilidades):
   python app.py
   A aplicacao fica disponivel em http://127.0.0.1:5000
3. Para usar o banco em um diretorio separado:
   export LAB_DB_PATH=/caminho/para/banco.db

## Variante do laboratorio
- scenario/vulnerable/app.py: mesma logica, mas a query SQL concatena a
  entrada do usuario. Use esta versao para demonstrar a falha.
- scenario/fixed/app.py: versao parametrizada (controlador).

## Avisos de seguranca
- NUNCA expor esta aplicacao na internet em um lab sem configuracao
  adicional de segregacao de rede.
- As senhas ficam em texto simples apenas para isolar o assunto SQL
  Injection; em producao, use Hash (Argon2id, bcrypt ou scrypt).
- O ambiente de desenvolvimento do Flask nao e um servidor de producao.

## Plano de testes de regressao
Rodar: python -m unittest discover -s tests
- Login legittimo continua funcionando.
- Payloads de SQL Injection (OR, comentario, UNION, stack queries) sao
  rejeitados na versao corrigida.
- O fluxo legittimo de cadastro e login nao sofreu regressao.
