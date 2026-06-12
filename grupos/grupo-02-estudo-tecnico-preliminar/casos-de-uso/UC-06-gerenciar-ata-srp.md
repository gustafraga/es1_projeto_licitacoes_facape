# UC-06 — Gerenciar Ata de Registro de Preços

## Identificação

| Campo | Valor |
|-------|-------|
| **ID** | UC-06 |
| **Nome** | Gerenciar Ata de Registro de Preços |
| **Ator Principal** | Servidor do setor de compras |
| **Atores Secundários** | Fornecedores registrados em ata |
| **Prioridade** | Média |
| **Origem** | Necessidade de controlar atas vigentes e adesões |

## Descrição Resumida

O servidor gerencia as Atas de Registro de Preços (SRP), consultando atas vigentes, registrando adesões e monitorando prazos de validade.

## Pré-condições

- Sistema possui atas registradas
- Servidor tem permissão para acessar atas

## Pós-condições

### Sucesso
- Ata consultada/gerenciada com sucesso
- Sistema registra a operação realizada

### Fracasso
- Operação não realizada
- Mensagem de erro exibida

## Fluxo Principal (Caminho Feliz)

| Passo | Ator | Ação |
|-------|------|------|
| 1 | Servidor | Acessa funcionalidade "Gerenciar Atas SRP" |
| 2 | Sistema | Exibe lista de atas cadastradas |
| 3 | Servidor | Aplica filtros (vigentes, por item, por fornecedor) |
| 4 | Sistema | Exibe atas conforme filtros |
| 5 | Servidor | Seleciona uma ata para visualizar |
| 6 | Sistema | Exibe detalhes da ata (itens, preços, validade, fornecedores) |
| 7 | Servidor | Registra adesão à ata (se for o caso) |
| 8 | Servidor | Atualiza saldo de itens consumidos |
| 9 | Sistema | Registra as alterações e logs |

## Fluxos Alternativos

### FA-01: Ver atas vencendo em 30 dias
- **Condição de ativação**: Servidor quer monitorar atas próximas do vencimento
- **A partir do passo**: 3
- **Passos**:
  1. Servidor seleciona filtro "Vencem nos próximos 30 dias"
  2. Sistema exibe atas com validade nos próximos 30 dias
  3. Servidor pode notificar fornecedores ou planejar renovação
- **Retorno ao fluxo principal**: Servidor seleciona outra ata

### FA-02: Calcular limite de adesão
- **Condição de ativação**: Servidor quer saber quanto ainda pode comprar via ata
- **A partir do passo**: 6
- **Passos**:
  1. Servidor clica em "Calcular saldo disponível"
  2. Sistema calcula: quantidade total - quantidade consumida
  3. Sistema exibe saldo disponível para adesão
- **Retorno ao fluxo principal**: passo 7

## Fluxos de Exceção

### FE-01: Ata expirada
- **Condição**: Servidor tenta registrar adesão em ata vencida
- **Tratamento**:
  1. Sistema verifica data de validade
  2. Sistema exibe "Ata expirada - adesão não permitida"
  3. Sistema bloqueia registro de adesão
- **Resultado**: Adesão não é registrada

### FE-02: Saldo insuficiente na ata
- **Condição**: Tentativa de adesão excede saldo disponível
- **Tratamento**:
  1. Sistema verifica saldo restante
  2. Sistema exibe "Saldo insuficiente na ata"
  3. Sistema sugere quantidade máxima permitida
  4. Servidor ajusta ou cancela
- **Resultado**: Adesão registrada apenas com quantidade ajustada

## Regras de Negócio Aplicáveis

- RN-01: Ata SRP tem validade máxima de 12 meses
- RN-02: Adesão não pode ultrapassar 100% do quantitativo inicial
- RN-03: Preços registrados em ata são fixos durante validade
- RN-04: Renovação de ata exige novo processo licitatório

## Requisitos Não-Funcionais Relevantes

- RNF-01: Sistema deve alertar atas com vencimento em 30, 15 e 7 dias
- RNF-02: Log de consultas e adesões deve ser registrado
- RNF-03: Exportação de atas em PDF disponível
