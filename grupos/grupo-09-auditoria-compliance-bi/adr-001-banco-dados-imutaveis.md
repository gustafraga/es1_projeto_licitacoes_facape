# ADR-001: Escolha do banco de dados para logs imutáveis

## Contexto
O módulo G09 precisa persistir todos os eventos recebidos dos módulos G01 a G08 de forma imutável, garantindo rastreabilidade e não-repúdio para fins de auditoria, conforme exigido pela Lei 14.133/2021.

## Decisão
Utilizaremos **PostgreSQL** com as seguintes estratégias:
- Tabela `evento_auditoria` configurada como **append-only** através de:
  - `REVOKE UPDATE, DELETE ON evento_auditoria FROM app_user;`
  - Uso de trigger que impede qualquer alteração ou exclusão.
- Chave primária `UUID` gerada pelo sistema.
- Particionamento mensal por `timestamp` para garantir desempenho.
- Índice em `(modulo_origem, timestamp)` para consultas frequentes.

## Alternativas consideradas
- **Amazon QLDB**: Rejeitado por lock-in com fornecedor e custo elevado.
- **Blockchain (Hyperledger)**: Overkill, complexidade desnecessária.
- **Arquivos de log rotacionados**: Difícil realizar consultas eficientes e garantir integridade.

## Consequências
- Necessidade de job de arquivamento/remoção de partições antigas (reter 5 anos por lei).
- Backups regulares da tabela são obrigatórios.
- Consultas analíticas podem exigir índ adicionais.
