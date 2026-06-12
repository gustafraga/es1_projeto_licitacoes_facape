# UC-02 — Consolidar Demandas em DFD

## Identificação

| Campo | Valor |
|-------|-------|
| **ID** | UC-02 |
| **Nome** | Consolidar Demandas em DFD |
| **Ator Principal** | Servidor do setor de compras |
| **Atores Secundários** | Nenhum |
| **Prioridade** | Alta |
| **Origem** | Necessidade de agrupar demandas para análise conjunta |

## Descrição Resumida

O servidor de compras consolida as demandas registradas pelas secretarias em um Documento de Formalização de Demanda (DFD).

## Pré-condições

- Existem demandas registradas com status "Aguardando consolidação"
- Servidor está autenticado como comprador

## Pós-condições

### Sucesso
- DFD gerado com todas as demandas do período
- Demandas consolidadas recebem status "Consolidadas"

### Fracasso
- Nenhum DFD é gerado
- Mensagem de erro é exibida

## Fluxo Principal (Caminho Feliz)

| Passo | Ator | Ação |
|-------|------|------|
| 1 | Servidor | Acessa funcionalidade "Consolidar Demandas" |
| 2 | Sistema | Exibe lista de demandas pendentes |
| 3 | Servidor | Seleciona período de consolidação (ex: mês atual) |
| 4 | Servidor | Filtra por secretaria (opcional) |
| 5 | Servidor | Clica em "Consolidar Selecionadas" |
| 6 | Sistema | Verifica se há pelo menos uma demanda selecionada |
| 7 | Sistema | Agrupa demandas em um DFD |
| 8 | Sistema | Gera número de identificação do DFD |
| 9 | Sistema | Atualiza status das demandas para "Consolidadas" |
| 10 | Sistema | Disponibiliza DFD para exportação (PDF/Excel) |

## Fluxos Alternativos

### FA-01: Filtrar demandas por secretaria
- **Condição de ativação**: Servidor quer consolidar apenas uma secretaria
- **A partir do passo**: 4
- **Passos**:
  1. Servidor seleciona uma secretaria específica no filtro
  2. Sistema exibe apenas demandas daquela secretaria
  3. Servidor prossegue com a consolidação
- **Retorno ao fluxo principal**: passo 5

## Fluxos de Exceção

### FE-01: Nenhuma demanda selecionada
- **Condição**: Servidor clica em consolidar sem selecionar demandas
- **Tratamento**:
  1. Sistema exibe mensagem "Selecione pelo menos uma demanda"
  2. Sistema não realiza consolidação
- **Resultado**: Nenhum DFD é gerado

## Regras de Negócio Aplicáveis

- RN-01: DFD só pode ser gerado com pelo menos 1 demanda
- RN-02: Demandas consolidadas não podem ser editadas individualmente
- RN-03: Cada demanda pertence a uma única secretaria

## Requisitos Não-Funcionais Relevantes

- RNF-01: Consolidação deve levar menos de 5 segundos para até 100 demandas
- RNF-02: DFD exportável em PDF e Excel
