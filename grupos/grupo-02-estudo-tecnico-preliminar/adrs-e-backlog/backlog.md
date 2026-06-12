#  Backlog — Sistema de Licitação

> **Módulo:** Cotação e Banco de Preços  
> **Responsável:** Pedro Ribeiro  
> **Data:** 01/06/2026

---

## 📌 Resumo das Histórias

| ID | Título | Prioridade |
|----|--------|:----------:|
| [US01](#us01----consultar-banco-de-preços) | Consultar Banco de Preços | 🔴 Alta |
| [US02](#us02----registrar-cotação-de-fornecedor) | Registrar Cotação de Fornecedor | 🔴 Alta |
| [US03](#us03----validar-especificação-técnica) | Validar Especificação Técnica | 🔴 Alta |
| [US04](#us04----detectar-preço-inexequível) | Detectar Preço Inexequível | 🟡 Média |
| [US05](#us05----gerar-estudo-técnico-preliminar-etp) | Gerar Estudo Técnico Preliminar (ETP) | 🟡 Média |

---

## Histórias de Usuário

---

### US01 — Consultar Banco de Preços

> **Como** analista de licitação, **quero** consultar o banco de preços automaticamente, **para** obter referências de valores de mercado sem precisar fazer pesquisa manual.

**Critérios de Aceitação:**

- [ ] O sistema retorna ao menos um preço de referência para o item pesquisado.
- [ ] A consulta registra data, hora e usuário que a realizou.
- [ ] Caso o item não seja encontrado, o sistema exibe mensagem clara ao usuário.

| Campo | Valor |
|-------|-------|
| **Prioridade** | 🔴 Alta |
| **Relacionado a** | ADR-001 (Integração via API) |

---

### US02 — Registrar Cotação de Fornecedor

> **Como** analista de licitação, **quero** registrar a cotação recebida de um fornecedor, **para** comparar propostas e embasar a escolha da melhor oferta.

**Critérios de Aceitação:**

- [ ] É possível registrar preço, prazo e fornecedor na cotação.
- [ ] O sistema impede o registro sem ao menos um preço e um fornecedor identificado.
- [ ] O sistema registra automaticamente quem cadastrou a cotação.

| Campo | Valor |
|-------|-------|
| **Prioridade** | 🔴 Alta |
| **Relacionado a** | ADR-002 (Auditoria por usuário autenticado) |

---

### US03 — ✅ Validar Especificação Técnica

> **Como** analista de licitação, **quero** validar se a especificação de um item está completa antes de abrir cotação, **para** evitar retrabalho por especificações mal formuladas.

**Critérios de Aceitação:**

- [ ] O sistema aponta campos obrigatórios faltando na especificação.
- [ ] A cotação só pode ser iniciada após a especificação ser validada.
- [ ] O resultado da validação fica registrado no histórico do item.

| Campo | Valor |
|-------|-------|
| **Prioridade** | 🔴 Alta |
| **Relacionado a** | — |

---

### US04 — ⚠️ Detectar Preço Inexequível

> **Como** gestor de licitação, **quero** que o sistema me alerte quando uma cotação estiver com preço muito abaixo da referência de mercado, **para** evitar selecionar propostas inexequíveis.

**Critérios de Aceitação:**

- [ ] O sistema compara o preço cotado com a referência do banco de preços.
- [ ] Preços abaixo de um limiar configurável geram alerta visível ao analista.
- [ ] O alerta não bloqueia o processo, mas fica registrado para fins de auditoria.

| Campo | Valor |
|-------|-------|
| **Prioridade** | 🟡 Média |
| **Relacionado a** | US01, ADR-001 |

---

### US05 — Gerar Estudo Técnico Preliminar (ETP)

> **Como** analista de licitação, **quero** gerar o Estudo Técnico Preliminar a partir dos dados de especificação e cotação já registrados, **para** não precisar preencher o documento manualmente.

**Critérios de Aceitação:**

- [ ] O ETP é gerado com os dados já inseridos no sistema, sem redigitação.
- [ ] O documento gerado identifica o responsável e a data de geração.
- [ ] É possível exportar o ETP em formato PDF ou equivalente.

| Campo | Valor |
|-------|-------|
| **Prioridade** | 🟡 Média |
| **Relacionado a** | US02, US03 |

---

## 🔑 Legenda

| Símbolo | Significado |
|:-------:|-------------|
| 🔴 | Alta prioridade |
| 🟡 | Média prioridade |
| - [ ] | Critério pendente de validação |
| - [x] | Critério validado |
