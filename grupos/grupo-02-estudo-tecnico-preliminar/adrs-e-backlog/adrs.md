# ADRs — Architecture Decision Records

> **Módulo:** Cotação e Banco de Preços  
> **Responsável:** Pedro Ribeiro  
> **Data:** 01/06/2026

---

## 📌 Resumo das Decisões

| ID | Título |
|----|--------|
| [ADR-001](#adr-001----integração-com-banco-de-preços-via-api) | Integração com Banco de Preços via API |
| [ADR-002](#adr-002----auditoria-de-cotações-por-registro-automático-de-usuário) | Auditoria de Cotações por Registro Automático de Usuário |

---

## Decisões

---

### ADR-001 — Integração com Banco de Preços via API

| Campo | Valor |
|-------|-------|
| **Número** | 001 |
| **Data** | 01/06/2026 |
| **Responsável** | Pedro Ribeiro |

---

#### Contexto

O sistema de licitação precisa consultar preços de referência de mercado para embasar cotações e validar propostas recebidas de fornecedores. Duas abordagens foram avaliadas para obter esses valores:

- Integração automática com uma API de banco de preços (ex: Painel de Preços do governo federal)
- Entrada manual dos valores pelo próprio analista de licitação

---

#### Decisão

> ✅ **Integrar o sistema com um banco de preços externo via API.**

A consulta de preços de referência será feita de forma automática, sem intervenção manual do analista para inserir os valores.

---

#### Justificativa

| Razão | Descrição |
|-------|-----------|
| **Rastreabilidade** | Cada consulta registra automaticamente a fonte, data e hora, criando um histórico auditável sem esforço adicional. |
| **Redução de erro humano** | A pesquisa e digitação manual está sujeita a erros de transcrição e viés, comprometendo a confiabilidade das referências. |
| **Eficiência** | A consulta automática é significativamente mais rápida, especialmente em licitações com múltiplos itens. |
| **Padronização** | Todos os analistas consultam a mesma fonte de dados, eliminando inconsistências entre cotações. |

---

#### Alternativas Consideradas

| Alternativa | Motivo da Rejeição |
|-------------|-------------------|
| **Entrada manual pelo analista** | Não gera rastro auditável da fonte utilizada, é lenta e abre margem para erros ou manipulação dos valores de referência. |

---

#### Consequências

- O sistema passa a depender da disponibilidade da API externa; quedas no serviço precisam ser tratadas com mensagens de erro claras.
- Todas as consultas ficam automaticamente vinculadas a uma fonte, data e usuário, fortalecendo a auditoria do processo.
- Reduz o trabalho manual do analista e diminui o risco de contestação dos preços utilizados.
- A equipe precisará configurar e manter a integração com a API, incluindo autenticação e tratamento de mudanças na estrutura dos dados retornados.

---

### ADR-002 — Auditoria de Cotações por Registro Automático de Usuário

| Campo | Valor |
|-------|-------|
| **Número** | 002 |
| **Data** | 01/06/2026 |
| **Responsável** | Pedro Ribeiro |

---

#### Contexto

O sistema precisa garantir rastreabilidade completa das operações de cotação — registrando quem realizou cada cotação, qual critério foi utilizado para selecionar uma proposta e quando cada ação ocorreu. Duas abordagens foram avaliadas:

- Registrar automaticamente o usuário autenticado em cada operação
- Disponibilizar um campo de preenchimento manual onde o analista informa o próprio nome

---

#### Decisão

> ✅ **O sistema registrará automaticamente o usuário autenticado em toda operação de cotação, seleção de proposta e validação de especificação.**

Não haverá campo manual para informar o responsável — a identidade será sempre capturada da sessão autenticada.

---

#### Justificativa

| Razão | Descrição |
|-------|-----------|
| **Confiabilidade da auditoria** | O registro automático elimina a possibilidade de omissão, erro ou falsificação do responsável pela operação. |
| **Conformidade** | Processos licitatórios exigem rastreabilidade das decisões; um campo manual não oferece garantia suficiente para auditoria formal. |
| **Responsabilização** | Vincular cada ação ao usuário autenticado cria responsabilidade individual clara, inibindo operações irregulares. |
| **Simplicidade de uso** | O analista não precisa preencher campos adicionais de identificação, reduzindo fricção no fluxo de trabalho. |

---

#### Alternativas Consideradas

| Alternativa | Motivo da Rejeição |
|-------------|-------------------|
| **Campo manual de responsável** | Permite que o campo seja deixado em branco, preenchido incorretamente ou atribuído a outra pessoa, tornando a auditoria não confiável. |

---

#### Consequências

- Toda operação de cotação exige que o usuário esteja autenticado; operações sem autenticação não serão permitidas.
- O histórico de ações fica automaticamente vinculado a usuários rastreáveis, facilitando auditorias internas e externas.
- A equipe precisará garantir que cada analista possua credenciais individuais — contas compartilhadas invalidam o propósito da rastreabilidade.
- Aumenta a percepção de responsabilidade individual, o que pode influenciar positivamente a qualidade das operações registradas.
