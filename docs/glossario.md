Glossário

Regra: a coluna "Minhas palavras" é preenchida por mim, sem copiar a definição. Revisar antes de entrevistas.

Módulo 0
Termo	Definição	Exemplo no projeto	Minhas palavras
AI Engineering	Construir sistemas confiáveis em torno de modelos prontos, tratando o modelo como componente não determinístico	Agente com prompt, guardrails, RAG e evals em volta do llama3.2	
Não determinismo	A mesma entrada pode gerar saídas diferentes	Três definições diferentes de "guardrail"	
Guardrail	Controle em tempo de execução que valida ou filtra a entrada e a saída do modelo	Módulos 3 e 7	
Eval-driven development	Definir como o sistema será avaliado antes de construí-lo	Dataset criado antes do agente	
Golden dataset	Conjunto curado de casos de teste que serve de critério de aceite	casos-de-teste.jsonl	
Rubrica	Critérios explícitos, definidos antes, para julgar uma resposta	Campo criterios	
Oráculo de teste	Mecanismo que decide se um teste passou; com LLMs não há saída exata para comparar	Juiz determinístico, LLM como juiz, humano	
Falso positivo (em teste)	O teste passa, mas o defeito existe	Critério que aprovava o "chute" no CT-005	
Baseline (linha de base)	Desempenho antes de uma melhoria, usado como referência	Rodada sem guardrails no Módulo 1	
Teste de regressão	Repetir os mesmos testes a cada mudança para garantir que nada quebrou	Rodar o dataset a cada módulo	
Validação de dataset	Checar a qualidade dos dados de teste (sintaxe, esquema, cobertura, qualidade)	validar_dataset.py	
Avaliação de sistema x de modelo	Sistema: a aplicação inteira no seu uso. Modelo: o LLM isolado em benchmarks	A vaga pede a de sistema	
Esquema (contrato de dados)	Regras de campos, tipos e valores que os dados devem seguir	8 campos obrigatórios	
Vocabulário controlado	Lista fechada de valores permitidos	pedir_esclarecimento, e não perguntar	
Garbage in, garbage out	A avaliação nunca é melhor que o dataset que a alimenta		
Caso multi-turno	Teste com histórico de conversa	Usuário cita o curso antes de perguntar a carga horária (Módulo 5)	
Dados sintéticos	Casos gerados por modelo; exigem curadoria humana		
Docs as code	Documentação versionada no Git junto ao código	Pasta docs/	
ADR	Registro curto de uma decisão de arquitetura: contexto, decisão, alternativas e consequências	docs/adr/	
Fonte única da verdade	Uma regra definida em um só lugar	tests/dataset/README.md	
Superfície de ataque	Conjunto de pontos por onde um sistema pode ser atacado	Ollama exposto em 0.0.0.0	
Secure by default	Configuração padrão já segura	Ollama escutando só em 127.0.0.1	
Dado pessoal x dado pessoal sensível	Pessoal: identifica alguém (CPF, nome). Sensível: lista do art. 5º, II da LGPD (saúde, religião, origem racial etc.)	CPF é pessoal, não sensível	
Princípio da necessidade	Tratar apenas os dados estritamente necessários (LGPD art. 6)	Chat não pede CPF	
Enumeração	Descobrir dados válidos testando valores, a partir das respostas do sistema	Testar CPFs alheios no CT-006	
Injeção indireta	Instrução maliciosa embutida em conteúdo, e não dita como ordem	CT-011; documentos do RAG no Módulo 6	
Defesa em profundidade	Várias camadas de controle, sem depender de uma só	Modelo + guardrail de saída + escape no front (CT-015)	
Hidden Context Exposure	OWASP-LLM08:2026; antigo "System Prompt Leakage"	CT-012	