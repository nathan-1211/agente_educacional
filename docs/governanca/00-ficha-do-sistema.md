# Ficha do Sistema - Assistente Educacional Horizonte

| Campo | Valor |
|---|---|
| Versão da ficha | 0.1 |
| Data | 17/11/2026 |
| Status do sistema | Protótipo de estudo. Não está em produção e não atende usuários reais. |
| Responsável técnico | Nathan Branco |
| Próxima revisão | Ao final de cada módulo da trilha, ou quando a finalidade mudar |

## 1. Finalidade e uso pretendido

Assistente conversacional que tira dúvidas de candidatos e alunos da Escola Horizonte de
Educação Profissional (instituição fictícia) sobre cursos livres: pré-requisitos, carga
horária, modalidade, horários e o passo a passo da matrícula.

O sistema **informa**. Ele **não decide** nada sobre a vida acadêmica ou financeira do usuário.

## 2. Fora do escopo (usos não permitidos)

| O sistema NÃO faz | Comportamento esperado | Motivo |
|---|---|---|
| Consultar matrícula, notas ou situação de aluno | Recusa e indica canal oficial | Não autentica o usuário; risco de enumeração e vazamento |
| Conceder, negar ou estimar bolsas, descontos e reembolsos | Encaminha para humano | Decisão com efeito financeiro deve ser humana |
| Cancelar matrícula | Encaminha para humano | Ato com efeito jurídico e financeiro |
| Coletar dados pessoais pelo chat | Orienta a não enviar | Princípio da necessidade (LGPD art. 6) |
| Responder assuntos alheios à escola | Recusa e redireciona | Uso fora da finalidade |
| Gerar HTML ou código executável | Responde em texto simples | Risco de XSS no front-end |

## 3. Usuários e partes afetadas

- **Usuários diretos:** candidatos, alunos e responsáveis legais.
- **Grupo de atenção especial:** adolescentes (menores de 18 anos), que podem usar o chat
  sem se identificar como tal. Dados de crianças e adolescentes têm proteção reforçada
  (LGPD art. 14; ECA).
- **Terceiros afetados:** professores e funcionários citados nas conversas.
- **Operadores:** equipe de atendimento/secretaria, que recebe os encaminhamentos.

## 4. Arquitetura (planejada)

| Componente | Tecnologia | Módulo |
|---|---|---|
| Modelo de linguagem | Llama 3.2 3B via Ollama, local | 1 |
| Orquestração | n8n | 1 |
| Observabilidade | Langfuse | 2 |
| Guardrail de entrada | Microsserviço Python (FastAPI) | 3 |
| Tools e MCP | n8n + Python | 4 |
| Memória | Postgres | 5 |
| Base de conhecimento (RAG) | Postgres + pgvector | 6 |
| Guardrail de saída | Python | 7 |
| Interfaces | HTML + Bootstrap; WhatsApp | 9 |

Decisões de arquitetura registradas em `docs/adr/`.

## 5. Dados tratados

| Dado | Origem | Observação |
|---|---|---|
| Mensagens dos usuários | Chat | Podem conter dados pessoais enviados espontaneamente (CPF, telefone, idade) |
| Base de conhecimento | Catálogo de cursos fictício | Sem dados pessoais. Não usa dados nem marca de instituição real |
| Registros (logs e traces) | Langfuse | Política de logs e retenção definida no Módulo 2 |
| Dataset de avaliação | `tests/dataset/` | Somente dados fictícios |

Base legal e retenção: a definir no Módulo 2. Em ambiente de estudo, nenhum dado real é tratado.

## 6. Classificação de risco

**Classificação proposta: risco baixo a limitado, com obrigação de transparência.**

Justificativa:
- O sistema apenas informa; não decide acesso, admissão, avaliação ou benefício financeiro.
- O PL 2338/2023 (aprovado no Senado, em tramitação na Câmara, **ainda não é lei**) adota
  abordagem baseada em risco e, no texto aprovado pelo Senado, trata como alto risco usos
  em educação ligados a decisões sobre acesso e avaliação de estudantes. O texto pode mudar.
- **Gatilho de reclassificação:** se o sistema passar a decidir ou recomendar concessão de
  bolsa, admissão ou avaliação de alunos, a classificação sobe para **alto risco** e exige
  avaliação de impacto e revisão humana obrigatória.

Obrigação legal vigente: LGPD (Lei 13.709/2018), sempre que houver dado pessoal.

## 7. Principais riscos identificados

Detalhamento na matriz de riscos (Módulo 1).

| Risco | Referência | Severidade |
|---|---|---|
| Informação inventada (alucinação) | OWASP-LLM07:2026 | Média a alta |
| Sequestro de instruções (prompt injection) | OWASP-LLM01:2026 | Crítica |
| Promessa de desconto, bolsa ou reembolso | OWASP-LLM03:2026 | Crítica |
| Exposição de dados pessoais | OWASP-LLM02:2026; LGPD | Crítica |
| Tratamento inadequado de menores | LGPD art. 14; ECA | Alta |
| Vazamento das instruções do sistema | OWASP-LLM08:2026 | Alta |
| XSS por saída do modelo | OWASP-LLM10:2026 | Crítica |
| Consumo excessivo de recursos | OWASP-LLM06:2026 | Média |

## 8. Transparência e supervisão humana

- O usuário deve ser informado de que conversa com uma IA (Módulo 9).
- Casos de bolsa, cancelamento, reclamação e situações sensíveis são encaminhados a uma
  pessoa (handoff).
- Nenhuma decisão com efeito sobre o usuário é tomada exclusivamente pelo sistema.

## 9. Avaliação

| Item | Situação |
|---|---|
| Dataset de casos de teste | v1: 16 casos, 12 categorias (`tests/dataset/casos-de-teste.jsonl`) |
| Validação do dataset | Automática (`tests/scripts/validar_dataset.py`) |
| Linha de base (baseline) | Pendente (Módulo 1) |
| Avaliação automatizada e red teaming | Pendente (Módulo 8) |
| Critério de aceite para produção | A definir com base na baseline |

## 10. Limitações conhecidas

- Modelo pequeno (3B parâmetros): mais propenso a erros factuais e a falhas de instrução.
- Comportamento não determinístico: a mesma pergunta gera respostas diferentes.
- Em teste preliminar (3 execuções), o modelo definiu "guardrail" corretamente em 1 de 3.
- Dataset v1 com um caso por categoria na maioria das categorias: insuficiente para
  conclusões estatísticas.
- Riscos LLM04, LLM05 e LLM09 não são cobertos pelo dataset de prompts; serão avaliados
  por auditoria de dependências e controle de acesso do RAG.

## 11. Referências

- NIST AI Risk Management Framework (AI RMF 1.0) - funções Govern, Map, Measure, Manage.
- ISO/IEC 42001:2023 - Sistema de gestão de IA.
- Lei 13.709/2018 (LGPD).
- PL 2338/2023 - Marco Legal da IA (em tramitação na Câmara dos Deputados).
- OWASP Top 10 for LLM Applications 2026 e OWASP Top 10 for Agentic Applications.

## Histórico

| Versão | Data | Alteração |
|---|---|---|
| 0.1 | 17/11/2026 | Criação: finalidade, escopo, riscos iniciais e dataset v1 |