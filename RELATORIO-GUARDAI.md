# GuardAI — Agente Inteligente para Cibersegurança e Análise de Vulnerabilidades

## 1. Apresentação

O GuardAI é um projeto educacional voltado à análise de vulnerabilidades em aplicações, com foco em práticas de AppSec (Application Security).

O laboratório foi desenvolvido utilizando Python, Flask e SQLite, permitindo demonstrar uma vulnerabilidade de SQL Injection e comparar seu comportamento antes e depois da correção.

## 2. Objetivo

Demonstrar como uma aplicação vulnerável pode permitir o contorno de autenticação por meio de SQL Injection e como consultas parametrizadas ajudam a prevenir esse tipo de falha.

## 3. Tecnologias utilizadas

- Python 3
- Flask 3.1.3
- SQLite
- Unittest
- Windows
- Ubuntu 24.04 LTS via WSL 2
- Hermes Agent

## 4. Escopo do laboratório

O ambiente foi desenvolvido exclusivamente para testes locais e controlados.

A aplicação possui duas implementações:

### Versão vulnerável

- Localizada em `scenario/vulnerable/app.py`.
- Utiliza concatenação de strings para construir consultas SQL.
- Permite demonstrar SQL Injection na autenticação.

### Versão corrigida

- Localizada em `app.py`.
- Utiliza consultas SQL parametrizadas.
- Trata as entradas do usuário como dados, evitando que alterem a estrutura da consulta.

## 5. Vulnerabilidade identificada

### SQL Injection — CWE-89

A vulnerabilidade ocorre quando entradas fornecidas pelo usuário são incorporadas diretamente a uma instrução SQL, sem parametrização adequada.

Na aplicação vulnerável, a consulta de autenticação utiliza concatenação de strings:

```python
sql = (
    "SELECT id, username FROM users "
    "WHERE username = '" + username
    + "' AND password = '" + password + "'"
)
```

Essa implementação permite que uma entrada especialmente construída altere a lógica da consulta.

## 6. Demonstração controlada

Foi utilizado o seguinte payload no laboratório:

```text
' OR '1'='1' --
```

O teste utiliza um banco SQLite temporário, dados fictícios e o `Flask test_client()`, sem abrir portas de rede ou acessar servidores externos.

### Resultados observados

| Teste | Resultado |
| --- | --- |
| Autenticação na versão vulnerável com payload | HTTP 200 |
| Autenticação na versão corrigida com o mesmo payload | HTTP 401 |
| Autenticação legítima na versão vulnerável | HTTP 200 |

O resultado demonstra que a versão vulnerável permite contornar a autenticação, enquanto a versão corrigida rejeita o mesmo payload.

## 7. Medida corretiva

A correção consiste em utilizar consultas parametrizadas.

Exemplo da implementação corrigida:

```python
row = conn.execute(
    "SELECT id, username FROM users WHERE username = ? AND password = ?",
    (username, password),
).fetchone()
```

Dessa forma, os valores recebidos são tratados como parâmetros, não como parte da estrutura SQL.

## 8. Validação e testes

Foram executados testes automatizados nos dois ambientes.

| Ambiente | Testes executados | Resultado |
| --- | ---: | --- |
| Windows | 6 | Aprovados |
| Ubuntu 24.04 / WSL 2 | 6 | Aprovados |

Também foi executada separadamente a bateria de três testes específicos de SQL Injection no Windows.

Todos os testes executados apresentaram resultado `OK`.

## 9. Evidências

As capturas de tela foram organizadas na pasta `evidence`:

- `01-testes-ubuntu.png` — testes automatizados no Ubuntu.
- `02-testes-windows.png` — testes automatizados no Windows.
- `03-sqli-comparacao-windows.png` — demonstração da vulnerabilidade e comparação com a versão corrigida.

## 10. Limitações e recomendações

O laboratório tem finalidade exclusivamente educacional.

Foram identificados os seguintes pontos de melhoria para uma aplicação real:

- Armazenar senhas utilizando algoritmos próprios para hashing, como Argon2id.
- Implementar validação de entradas.
- Adotar tratamento seguro de erros.
- Utilizar configurações apropriadas para produção.
- Implementar logs de segurança e monitoramento.
- Realizar novos testes de segurança após cada alteração.

As senhas do laboratório estão armazenadas em texto simples e não devem ser utilizadas como referência para sistemas reais.

## 11. Conclusão

O projeto demonstrou, em ambiente controlado, como uma vulnerabilidade de SQL Injection pode comprometer a autenticação de uma aplicação.

A comparação entre as duas implementações evidenciou a importância das consultas parametrizadas como medida de prevenção.

A validação foi realizada no Windows e no Ubuntu, com aprovação dos testes automatizados nos dois ambientes.

O laboratório representa uma etapa prática de aprendizado em desenvolvimento seguro, análise de vulnerabilidades e fundamentos de AppSec.

---

**Projeto:** GuardAI — Agente Inteligente para Cibersegurança e Análise de Vulnerabilidades  
**Desafio:** DIO  
**Responsável:** Gabriela Alves
