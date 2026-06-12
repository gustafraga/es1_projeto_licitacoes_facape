# Grupo 09 — Auditoria, Compliance e Indicadores de Negócio

## Módulo do Sistema

Módulo centralizado que registra todos os eventos de todos os módulos (G01–G08), valida conformidade com a Lei 14.133/2021 e gera indicadores de desempenho.

## Responsabilidade

- Receber eventos de todos os módulos: criação, modificação, envio, recepção, resultado
- Registrar trilha de auditoria imutável (quem, quando, o quê, resultado)
- Validar conformidade: todas as operações seguem a Lei 14.133/2021?
- Calcular indicadores: tempo médio de processamento, taxa de sucesso, variação de preços
- Gerar alertas: processo travado? Prazo ultrapassado?

**Entradas:** Eventos de G01–G08 (logs, mudanças de estado)  
**Saídas:** Logs de auditoria, relatórios de conformidade, indicadores, alertas

---

## Entregas Mínimas

| Artefato | Descrição |
|----------|-----------|
| Casos de uso (mínimo 4) | Registrar evento, gerar relatório de conformidade, calcular indicadores, enviar alertas |
| Diagrama UML de classes | `EventoAuditoria`, `LogOperacao`, `ConformidadeItem`, `Indicador`, `Alerta` |
| Diagrama de sequência | Integração com todos os módulos |
| BPMN | Fluxo de auditoria contínua, geração periódica de relatórios |
| Backlog | Mínimo 5 histórias de usuário |
| ADRs (mínimo 2) | Ex.: Event Sourcing? Qual banco para logs imutáveis? |
| Testes | Integridade de logs, cálculo correto de indicadores |
| Auditoria | Meta-auditoria: quem acessou os logs de auditoria |

---

## Interfaces com Outros Módulos

- **Entrada ← G01 a G08:** Eventos de todos os módulos

---

## Observação

Este grupo pode opcionalmente incluir um arquivo `contexto-agente.md` apenas para resumir seu próprio módulo. Nenhum grupo tem como tema principal artefatos para agentes de IA.

---

## Decisões Arquiteturais (ADRs)

- **ADR-001: Banco de dados para logs imutáveis** – Utilizamos PostgreSQL com tabela `evento_auditoria` configurada como append-only (revoke update/delete), particionamento mensal e índices em `(modulo_origem, timestamp)`. Alternativas como Amazon QLDB e blockchain foram rejeitadas por custo e complexidade.
- **ADR-002: Event Sourcing vs. log simples** – Optamos por um log append-only simples sem Event Sourcing completo, pois não há necessidade de reconstruir estado de agregados; cada módulo mantém seu próprio estado atual. Isso reduz complexidade e mantém os requisitos de auditoria.

## Entrega do Grupo

> Preencha esta seção ao finalizar:

- **Integrantes:** Kelvin Fernandes, Luis Felipe, Matheus Henrique, Gustavo Fraga, João Pedro Carvalho
- **Data de entrega:** 03/06/2026
- **Branch/PR:** feature/grupo-09-auditoria-compliance-bi
