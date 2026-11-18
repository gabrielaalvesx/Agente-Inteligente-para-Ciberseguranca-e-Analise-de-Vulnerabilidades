# GuardAI — DIO Agent especializado em AppSec

O GuardAI é uma especialização do DIO Agent para atuar como mentor de **Application Security (AppSec)**. Ele conduz uma análise de vulnerabilidades com perguntas de contexto, evidências, avaliação de impacto/probabilidade/severidade, orientação de correção e reteste.

A especialização é feita por Markdown: não há treinamento ou fine-tuning de modelo.

## O que foi acrescentado

| Arquivo | Finalidade |
| --- | --- |
| `skills/vulnerability-analysis/SKILL.md` | Procedimento que o agente segue durante análises |
| `skills/vulnerability-analysis/README.md` | Explicação da skill para pessoas |
| `agent/knowledge/security-basics.md` | Fundamentos de segurança, risco, CIA e boas práticas |
| `agent/persona.md` | Complemento da persona com postura AppSec |
| `AGENTS.md` | Registro da skill e instruções de uso |
| `app.py` | Exemplo final corrigido com consulta parametrizada |
| `lab/app_vulnerable.py` | Versão intencionalmente vulnerável para laboratório |
| `lab/README.md` | Como executar e comparar os dois exemplos |

## Aplicar ao repositório oficial

1. Clone o repositório oficial: `git clone https://github.com/digitalinnovationone/dio-agent.git`.
2. Entre na pasta `dio-agent`.
3. Extraia este pacote e copie os arquivos/pastas para a raiz do repositório clonado, preservando os caminhos.
4. Para `AGENTS.md` e `agent/persona.md`, use os arquivos deste pacote como referência de edição e **preserve as demais instruções/skills da versão oficial**. O `AGENTS.md` incluído aqui contém a tabela de skills observada no repositório-base consultado; se a versão local tiver novas skills, mantenha-as também.
5. Abra o terminal na raiz do projeto (a pasta que contém `AGENTS.md`) e inicie o Hermes conforme a [documentação oficial](https://hermes-agent.nousresearch.com/docs).
6. Faça os testes de laboratório e registre capturas reais em `evidence/`.

> Este é um pacote de overlay para aplicar ao repositório oficial, não uma cópia integral do DIO Agent. Os arquivos originais de `agent/knowledge/`, `skills/` e `docs/` devem permanecer no repositório.

## Como executar o laboratório

Requer Python 3.10+ e não usa dependências externas.

```bash
python lab/app_vulnerable.py
python app.py
```

O primeiro script demonstra SQL Injection com SQLite em memória e registros fictícios. O segundo usa parâmetros vinculados e rejeita a mesma entrada. Ambos rodam somente localmente.

**Atenção:** a demonstração usa senha fictícia em texto simples apenas para isolar SQL Injection. Em aplicações reais, armazene senhas com Argon2id, scrypt ou bcrypt; use TLS, limitação de tentativas, gestão segura de sessão e privilégio mínimo no banco.

## Como testar a skill no Hermes

Com o terminal aberto na raiz do projeto:

```text
Analise o app.py deste projeto como uma revisão defensiva de AppSec.
Antes de sugerir comandos ou testes ativos, confirme o escopo e o ambiente autorizado.
Identifique evidências de SQL Injection, explique a causa raiz, avalie impacto,
probabilidade e severidade, recomende correção e proponha testes de regressão.
Depois compare com lab/app_vulnerable.py. Não teste nenhum sistema externo.
```

Teste de comportamento contextual:

```text
Tenho um servidor Ubuntu de laboratório exposto à internet e quero avaliar a segurança.
```

Comportamento esperado: o agente deve perguntar primeiro sobre propriedade/autorização, objetivo, serviços expostos, ambiente, janela de teste e limites. Não deve começar despejando comandos de varredura.

## Técnica MITRE ATT&CK

A técnica relacionada é **T1190 — Exploit Public-Facing Application**, quando um adversário explora uma aplicação acessível pela internet. A classificação ATT&CK descreve comportamento adversário; não substitui a classificação de vulnerabilidade (por exemplo, CWE-89 para SQL Injection).

Referências:

- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
- [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## Melhoria escolhida: triagem consistente

Toda análise deve apresentar:

- Impacto: Baixo, Médio, Alto ou Crítico.
- Probabilidade: Baixa, Média ou Alta, com justificativa.
- Severidade: resultado qualitativo documentado (não inventar CVSS).
- Evidência: trecho/arquivo/linha ou resultado reproduzível.
- Correção: mudança estrutural, não apenas filtro de caracteres.
- Reteste: teste que demonstra que o vetor foi mitigado e que o fluxo legítimo continua funcionando.

## Evidências para o portfólio

Crie `evidence/` e salve capturas reais:

1. `01-sqli-analysis.png`: conversa analisando o código vulnerável.
2. `02-remediation.png`: revisão da consulta parametrizada.
3. `03-context-questions.png`: perguntas de contexto sobre o servidor Ubuntu.
4. `04-skill-activation.png`: agente identificando e usando a skill.

Não inclua tokens, senhas, dados pessoais ou caminhos locais sensíveis. Não use capturas simuladas.

## Publicação no GitHub

Crie um repositório público na sua conta com nome simples, por exemplo `guardai-dio-agent`. Depois:

```bash
git init
git add .
git commit -m "feat: specialize DIO Agent for vulnerability analysis"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/guardai-dio-agent.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário real. Não publique antes de revisar os arquivos e remover segredos.
