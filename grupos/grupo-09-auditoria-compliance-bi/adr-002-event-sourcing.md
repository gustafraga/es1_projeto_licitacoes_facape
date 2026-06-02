# ADR-002: Uso de Event Sourcing vs. Log simples

## Contexto
O sistema precisa registrar todas as mudanças de estado dos processos licitatórios para auditoria. Existe a possibilidade de implementar um padrão de Event Sourcing completo, onde o estado atual seria reconstruído a partir dos eventos.

## Decisão
**Não adotar Event Sourcing completo.** Optamos por um modelo de **log append-only** simples (tabela de eventos) sem reconstrução de estado agregado.

## Justificativa
- Não há necessidade de "replay" de eventos para recriar o estado de negócio – cada módulo já mantém seu próprio estado atual.
- A auditoria exige apenas o registro histórico imutável, não a derivação de estado por eventos.
- Menor complexidade de implementação e manutenção.
- O banco relacional com tabela de eventos atende todos os requisitos de consulta.

## Alternativas rejeitadas
- **Event Sourcing completo (ex.: usando EventStoreDB)**: Aumentaria a complexidade e o custo, sem benefício claro para o escopo.

## Consequências
- Cada módulo é responsável por sua própria base de estado atual.
- G09 mantém apenas o log histórico, não o estado agregado.
- Se no futuro precisarmos de auditoria por agregação, teremos que implementar uma camada de leitura específica.
