# Meta-auditoria – Controle de Acesso aos Logs de Auditoria

## Objetivo
Garantir rastreabilidade de **quem consultou a trilha de auditoria**, quando e com quais filtros, prevenindo acessos não autorizados ou suspeitos.

## Estratégia de Implementação

### Tabela `acesso_auditoria`
| Campo | Tipo | Descrição |
|-------|------|-------------|
| id | UUID | Chave primária |
| usuario | VARCHAR(100) | Login ou e-mail do usuário autenticado |
| timestamp | TIMESTAMP | Data e hora da consulta (UTC) |
| filtros_utilizados | JSON | Parâmetros da consulta (ex: `{"modulo":"G03","dataInicio":"2025-01-01"}`) |
| ip_origem | INET | Endereço IP da requisição |
| endpoint_consultado | VARCHAR(100) | Endpoint acessado (`/eventos`, `/relatorios/conformidade`) |
| quantidade_registros | INTEGER | Número de eventos retornados |

### Regras de Negócio
1. **Registro obrigatório**: Toda requisição aos endpoints de leitura da auditoria (`GET /eventos`, `GET /relatorios`) deve inserir um registro nesta tabela **antes** de retornar os dados.
2. **Imutabilidade**: A tabela `acesso_auditoria` também é append-only (não permite UPDATE/DELETE).
3. **Privilégios**: Apenas usuários com papel `super_auditor` podem consultar a meta-auditoria.
4. **Retenção**: Os registros de acesso são mantidos por 5 anos (mesmo prazo dos logs de auditoria).

### Exemplo de Registro (JSON)
```json
{
  "id": "a1b2c3d4-...",
  "usuario": "auditor.jose@facape.br",
  "timestamp": "2026-06-02T14:30:00Z",
  "filtros_utilizados": {"modulo": "G04", "dataInicio": "2026-05-01", "dataFim": "2026-05-31"},
  "ip_origem": "200.137.68.42",
  "endpoint_consultado": "/eventos",
  "quantidade_registros": 127
}
