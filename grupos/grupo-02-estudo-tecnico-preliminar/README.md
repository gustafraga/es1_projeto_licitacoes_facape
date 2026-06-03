# Grupo 02 — Estudo Técnico Preliminar (ETP)

## Módulo do Sistema

Análise técnica do DFD: cotação de preços (via Banco de Preços), especificação refinada e análise de mercado.

## Responsabilidade

- Receber DFD consolidado (G01)
- Consultar Banco de Preços para obter 3+ cotações por item
- Refinar especificação técnica (normas, padrões, garantias)
- Gerar ETP com recomendações de parcelamento

**Entradas:** DFD (G01)  
**Saídas:** ETP com cotações, especificação e análise de mercado

---

## Entregas Mínimas

| Artefato | Descrição | Status |
|----------|-----------|--------|
| Casos de uso (mínimo 4) | Consultar Banco de Preços, fazer cotação, validar especificação, gerar ETP | ✅ Concluído |
| Diagrama UML de classes | `Cotacao`, `Fornecedor`, `Especificacao`, `AnaliseETP` | ✅ Concluído |
| Diagrama de sequência | Integração com Banco de Preços, análise de propostas | ✅ Concluído |
| BPMN | Fluxo de análise técnica com pontos de validação | ✅ Concluído |
| Backlog | Mínimo 5 histórias de usuário | ✅ Concluído |
| ADRs (mínimo 2) | Ex.: API vs. manual para Banco de Preços | ✅ Concluído |
| Testes | Validação de cotações, detecção de outliers de preço | ✅ Concluído |
| Auditoria | Quem fez cada cotação, critério de seleção | ✅ Concluído |

---

## Interfaces com Outros Módulos

- **Entrada ← G01 (DFD):** DFD consolidado
- **Saída → G03 (Atas SRP):** ETP
- **Saída → G04 (TR):** ETP

---

## Integrantes

| Nome | Matrícula |
|------|-----------|
| Luan Regis Monteiro | 26460 |
| Luiz Eduardo Fernandes Cruz  | 26274 |
| Pedro Guilherme Rodrigues Ribeiro  | 25396 |
| Giancarlo Ribeiro Barbosa Filho  | 26375 |
| Adriel Henry Valeriano Rodrigues | 26424 |

---

## Decisões Tomadas

O Grupo 02 optou por estruturar os casos de uso seguindo o template padronizado, com identificação, fluxo principal, fluxos alternativos, exceções, regras de negócio e requisitos não-funcionais.

Decidimos focar primeiro nos 6 casos de uso obrigatórios para garantir cobertura completa do módulo ETP:
- UC-01 e UC-02: entrada do sistema (registro e consolidação de demandas)
- UC-03: core do ETP (cotação de preços)
- UC-04, UC-05 e UC-06: saída para outros módulos (TR, OF e atas)

A principal dificuldade foi equilibrar o detalhamento dos fluxos sem torná-los complexos. A solução foi manter 1-2 fluxos alternativos e 1 exceção por caso de uso.

---

## Limitações Identificadas

- Diagramas de sequência e BPMN pendentes
- Backlog de histórias de usuário pendente
- ADRs não documentadas
- Contrato de integração com G01, G03 e G04 será definido após alinhamento
- Testes de integração pendentes
- Formatação dos .md pode ser refinada posteriormente

---

## 📁 Estrutura da Pasta

- `grupo-02-estudo-tecnico-preliminar/`
  - `README.md`
  - `UC-01-registrar-demanda.md`
  - `UC-02-consolidar-dfd.md`
  - `UC-03-realizar-cotacao.md`
  - `UC-04-elaborar-tr.md`
  - `UC-05-emitir-ordem-fornecimento.md`
  - `UC-06-gerenciar-ata-srp.md`
  - `diagrama-classes-g02.drawio`
  - `diagrama-classes-g02.png`


---

## Data de Entrega

30/05/2026

## Link do PR

...
