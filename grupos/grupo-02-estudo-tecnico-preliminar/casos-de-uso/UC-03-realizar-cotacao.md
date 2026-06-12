# UC-03 — Realizar Cotação de Preços

## Identificação

| Campo | Valor |
|-------|-------|
| **ID** | UC-03 |
| **Nome** | Realizar Cotação de Preços |
| **Ator Principal** | Servidor do setor de compras |
| **Atores Secundários** | Banco de Preços (sistema externo), Fornecedores |
| **Prioridade** | Alta |
| **Origem** | Necessidade do ETP de obter preços de mercado |

## Descrição Resumida

O servidor pesquisa preços de um item no Banco de Preços, registra pelo menos 3 cotações e calcula o valor médio para subsidiar o Estudo Técnico Preliminar.

## Pré-condições

- O DFD do item já foi recebido do G01
- O item tem especificação básica definida

## Pós-condições

### Sucesso
- Pelo menos 3 cotações registradas
- Preço médio calculado e armazenado
- Cotação vinculada ao DFD do item

### Fracasso
- Nenhuma cotação é registrada
- Sistema registra log de erro

## Fluxo Principal (Caminho Feliz)

| Passo | Ator | Ação |
|-------|------|------|
| 1 | Servidor | Acessa funcionalidade "Realizar Cotação" |
| 2 | Sistema | Exibe formulário com dados do DFD (item, quantidade) |
| 3 | Servidor | Informa critérios de pesquisa (marca, região, prazo) |
| 4 | Sistema | Consulta o Banco de Preços externo |
| 5 | Sistema | Exibe lista de fornecedores e preços encontrados |
| 6 | Servidor | Seleciona pelo menos 3 cotações |
| 7 | Sistema | Calcula automaticamente o preço médio |
| 8 | Servidor | Confirma e salva a cotação |
| 9 | Sistema | Gera o ETP com os preços registrados |

## Fluxos Alternativos

### FA-01: Pesquisa retorna menos de 3 cotações
- **Condição de ativação**: Banco de Preços retorna 0, 1 ou 2 resultados
- **A partir do passo**: 5
- **Passos**:
  1. Sistema exibe mensagem "Poucos resultados encontrados"
  2. Sistema pergunta se deseja ampliar critérios
  3. Servidor amplia região ou remove filtros
  4. Sistema refaz a consulta
- **Retorno ao fluxo principal**: passo 5

### FA-02: Cotação manual
- **Condição de ativação**: Banco de Preços indisponível ou item não cadastrado
- **A partir do passo**: 4
- **Passos**:
  1. Sistema permite entrada manual de preços
  2. Servidor pesquisa preços em sites de fornecedores
  3. Servidor digita fornecedor, preço e data
  4. Servidor repete para obter 3 cotações
- **Retorno ao fluxo principal**: passo 6

## Fluxos de Exceção

### FE-01: Banco de Preços indisponível
- **Condição**: API do Banco de Preços não responde
- **Tratamento**:
  1. Sistema exibe mensagem "Serviço indisponível"
  2. Sistema registra log para auditoria
  3. Sistema sugere modo de cotação manual
  4. Servidor decide se aguarda ou usa manual
- **Resultado**: Cotação continua em modo manual ou é cancelada

### FE-02: Fornecedor não encontrado
- **Condição**: Servidor digita fornecedor inexistente na cotação manual
- **Tratamento**:
  1. Sistema exibe "Fornecedor não cadastrado"
  2. Sistema oferece opção de cadastrar novo fornecedor
  3. Servidor cadastra ou corrige nome
- **Resultado**: Cotação prossegue após correção

## Regras de Negócio Aplicáveis

- RN-01: Toda cotação deve ter no mínimo 3 fornecedores consultados
- RN-02: Cotação deve ser válida por 30 dias
- RN-03: Preço médio é calculado pela média aritmética simples
- RN-04: Cotações com preço 30% acima da média são sinalizadas como alerta

## Requisitos Não-Funcionais Relevantes

- RNF-01: Consulta ao Banco de Preços deve responder em até 5 segundos
- RNF-02: Log de toda cotação deve ser registrado para auditoria (G09)
- RNF-03: Sistema deve registrar usuário, data e critérios de cada cotação
