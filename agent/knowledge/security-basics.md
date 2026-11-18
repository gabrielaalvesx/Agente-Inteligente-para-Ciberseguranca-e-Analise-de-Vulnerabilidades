# Fundamentos de Cibersegurança e AppSec

## Conceitos essenciais

### Ativo
Recurso com valor para uma organização ou pessoa: aplicação, servidor, banco de dados, credencial, serviço, dispositivo ou informação.

### Ameaça
Circunstância ou agente capaz de causar dano a um ativo. Exemplos: atacante externo, erro operacional, malware ou falha de fornecedor.

### Vulnerabilidade
Fraqueza em software, configuração, processo ou controle que pode ser explorada ou acionada por uma ameaça.

### Risco
Combinação contextual entre probabilidade de um evento e impacto caso ele ocorra. Não é sinônimo de vulnerabilidade: uma falha é uma condição; risco considera contexto, exposição e consequências.

### Exploit
Técnica, sequência ou código que aproveita uma vulnerabilidade. A existência de uma vulnerabilidade não significa que toda exploração seja viável em qualquer contexto.

## Tríade CIA
- **Confidencialidade:** somente entidades autorizadas acessam a informação.
- **Integridade:** dados e sistemas permanecem corretos e não são alterados indevidamente.
- **Disponibilidade:** sistemas e dados ficam acessíveis quando necessários.

Um achado pode afetar uma ou mais dimensões. SQL Injection, por exemplo, pode comprometer confidencialidade e integridade e, dependendo do contexto, disponibilidade.

## Avaliação de risco
Avalie separadamente:

### Impacto
- **Baixo:** efeito limitado, dados não sensíveis e recuperação simples.
- **Médio:** impacto restrito em dados, usuários ou operação.
- **Alto:** exposição relevante, alteração não autorizada ou interrupção significativa.
- **Crítico:** comprometimento amplo de dados/sistemas ou impacto severo em serviço essencial.

### Probabilidade
- **Baixa:** exige condições improváveis, acesso restrito ou múltiplas barreiras.
- **Média:** depende de condições plausíveis, mas existem barreiras ou pré-requisitos.
- **Alta:** vetor acessível, baixa complexidade e poucas barreiras conhecidas.

### Severidade
Consolide impacto e probabilidade com justificativa contextual. Não invente pontuação CVSS. Se os dados forem insuficientes, declare a classificação como preliminar e peça as informações que faltam.

## SQL Injection
SQL Injection ocorre quando dados não confiáveis são incorporados à estrutura de uma consulta SQL, permitindo que a entrada altere sua lógica.

### Causa comum
Concatenação ou interpolação de strings para montar instruções SQL com dados fornecidos pelo usuário.

### Prevenção
- Use consultas parametrizadas (prepared statements) com parâmetros vinculados.
- Não concatene entrada externa na estrutura SQL.
- Para identificadores dinâmicos que não aceitam parâmetros, use allowlist estrita.
- Aplique privilégio mínimo à conta do banco.
- Trate erros sem expor consultas, credenciais ou detalhes internos.
- Validação de entrada é complementar e não substitui parametrização.

### Referências
- CWE-89: Improper Neutralization of Special Elements used in an SQL Command: https://cwe.mitre.org/data/definitions/89.html
- OWASP SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

## Boas práticas gerais
- Princípio do menor privilégio.
- Defesa em profundidade.
- Gestão segura de segredos; nunca versionar tokens ou senhas.
- Criptografia em trânsito (TLS) e proteção adequada em repouso.
- Autenticação robusta e armazenamento de senhas com hash adaptativo (Argon2id, scrypt ou bcrypt).
- Atualização de dependências e correções de segurança.
- Logs úteis sem segredos ou dados sensíveis.
- Backup e plano de recuperação testados.
- Revisão de código e testes de segurança no ciclo de desenvolvimento.
- Separação entre desenvolvimento, homologação e produção.

## Segurança de testes
- Confirme autorização, ativo, ambiente e escopo antes de testes ativos.
- Use ambientes próprios ou explicitamente autorizados.
- Prefira dados fictícios e laboratório local.
- Evite ações destrutivas e respeite limites operacionais.
- Registre evidências sanitizadas e resultados reproduzíveis.

## MITRE ATT&CK
MITRE ATT&CK é uma base de conhecimento de táticas e técnicas observadas em atividades adversárias. Use-a para contextualizar comportamento, não como substituta de CWE, CVSS ou avaliação de risco.

Para exploração de aplicações expostas publicamente, a técnica relevante pode ser **T1190 — Exploit Public-Facing Application**: https://attack.mitre.org/techniques/T1190/
