# Argus — Casos de Uso

## Atores

| Ator | Quem é | O que faz na plataforma |
| :--- | :--- | :--- |
| **Visitante** | Qualquer pessoa sem conta | Pesquisa e consulta o catálogo público |
| **Investigador** | Utilizador registado que consome dados | Descarrega datasets, pede acesso a privados, avalia e reporta |
| **Contribuidor** | Investigador que também produz dados | Submete datasets, gere versões e decide pedidos de acesso |
| **Moderador** | Curador técnico da plataforma | Valida certificações, comprovativos e trata denúncias |
| **Administrador** | Equipa de governação | Gere utilizadores, papéis e catálogos de referência |

> O **Contribuidor** herda todas as capacidades do **Investigador** e adiciona as de publicação e gestão.

---

## Casos de Uso

### Visitante
| ID | Caso de Uso |
| :- | :--- |
| V1 | Pesquisar datasets |
| V2 | Consultar ficha técnica |
| V3 | Pré-visualizar sinal |
| V4 | Consultar rankings |
| V5 | Criar conta |

### Investigador
| ID | Caso de Uso | Notas |
| :- | :--- | :--- |
| I1 | Descarregar dataset | Verifica permissão de acesso |
| I2 | Pedir acesso a dataset privado | Se preço > 0 €, tem de anexar comprovativo de pagamento |
| I3 | Avaliar qualidade (review) | Requer histórico de download |
| I4 | Reportar problema | — |
| I5 | Comparar datasets | — |

### Contribuidor *(herda I1 a I5)*
| ID | Caso de Uso | Notas |
| :- | :--- | :--- |
| C1 | Submeter dataset público | Valida CSV + gera relatório de qualidade (Q) |
| C2 | Registar dataset privado | Valida CSV + gera relatório de qualidade (Q) |
| C3 | Solicitar certificação | Só disponível após publicação e sem pedido aberto |
| C4 | Decidir pedido de acesso gratuito | Concede acesso de forma atómica (RN-12) |
| C5 | Publicar nova versão | Valida CSV |

### Moderador
| ID | Caso de Uso | Notas |
| :- | :--- | :--- |
| M1 | Validar certificação | Regista decisão em auditoria |
| M2 | Validar comprovativo de acesso | Concede acesso de forma atómica (RN-12) |
| M3 | Tratar reports | Se a infração for grave, pode despublicar o dataset |
| M4 | Moderar reviews | Regista decisão em auditoria |
| M5 | Sinalizar utilizador | — |

### Administrador
| ID | Caso de Uso | Notas |
| :- | :--- | :--- |
| A1 | Gerir utilizadores | — |
| A2 | Gerir papéis | Regista decisão em auditoria |
| A3 | Tratar utilizadores sinalizados | Regista decisão em auditoria |
| A4 | Consultar painel global | — |
| A5 | Gerir catálogos de referência | Sensores, unidades, plataformas, licenças |

---

## Cenários dos Fluxos Críticos

### C1 — Submeter Dataset Público
**Ator:** Contribuidor | **Pré-condição:** Sessão iniciada com papel de Contribuidor

1. O contribuidor acede ao assistente de submissão (3 passos).
2. Carrega o ficheiro CSV.
3. O sistema valida o ficheiro: UTF-8, separador vírgula, primeira coluna `timestamp` com valores estritamente crescentes.
4. O sistema calcula a nota de qualidade $Q$ e gera uma amostra para pré-visualização.
5. O contribuidor preenche os metadados: título, descrição, plataforma, licença, tags e mapeamento de sensores.
6. O contribuidor declara a integridade dos dados e confirma.
7. O sistema grava o ficheiro em `storage/datasets/` e cria os registos na base de dados.

**Exceção — CSV inválido:** O sistema rejeita o ficheiro com indicação da linha e coluna do erro. O contribuidor corrige e volta ao passo 2.  
**Exceção — Lacunas ou ruído detetados:** O sistema avisa e reduz a nota $Q$, mas não bloqueia a submissão.

**Pós-condição:** Dataset no estado `Publicado`, versão 1 imutável, nota $Q$ calculada.

---

### I2 — Pedir Acesso a Dataset Privado
**Ator:** Investigador | **Pré-condição:** Sessão iniciada; sem pedido ativo para este dataset

1. O investigador clica em "Pedir Acesso" na ficha do dataset.
2. Preenche a justificação do pedido e submete.
3. Se o preço for 0 €, o pedido é registado como `pendente` e enviado ao contribuidor para decisão (C4).
4. Se o preço for > 0 €, o sistema pede o comprovativo de pagamento (PDF/PNG/JPG até 2 MB) e encaminha para a moderação (M2).

**Exceção:** Se já existir um pedido ativo, o sistema recusa e informa o investigador.

**Pós-condição:** Pedido criado em `access_requests` com estado `pendente` ou `em_validação`.

---

### M2 — Validar Comprovativo de Acesso *(Transação Atómica — RN-12)*
**Ator:** Moderador | **Pré-condição:** Sessão iniciada com papel de Moderador; pedido no estado `em_validação`

1. O moderador abre o pedido na fila de moderação.
2. Consulta os detalhes e visualiza o comprovativo de pagamento.
3. Aprova ou recusa com nota obrigatória.
4. **Se aprovar:** o sistema executa numa única transação atómica:
   - Bloqueia a linha do pedido (`SELECT ... FOR UPDATE`);
   - Atualiza o estado para `aprovado`;
   - Cria o registo de acesso em `dataset_access`;
   - Grava o evento no `audit_log`.

**Exceção — Aprovação simultânea:** Se dois moderadores tentarem aprovar ao mesmo tempo, apenas um tem sucesso. O outro recebe uma notificação de conflito e o pedido já está resolvido.

**Pós-condição:** O investigador tem acesso imediato ao download. Evento auditado.

---

### M3 — Tratar Reports
**Ator:** Moderador | **Pré-condição:** Sessão iniciada com papel de Moderador; report no estado `aberto`

1. O moderador consulta a denúncia e os detalhes do dataset associado.
2. Se a infração for ligeira, notifica o contribuidor para correção e resolve o report.
3. Se a infração for grave (dados falsos, violação de privacidade), pode despublicar o dataset:
   - O dataset passa a estado `despublicado` e sai do catálogo imediatamente.
   - O dataset **nunca é apagado** da base de dados (preserva integridade histórica).
   - A ação fica registada no `audit_log`.

**Pós-condição:** Report resolvido; dataset pode estar despublicado. Evento auditado.
