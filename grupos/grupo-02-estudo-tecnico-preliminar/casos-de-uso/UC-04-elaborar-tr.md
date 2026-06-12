# UC-04 — Elaborar Termo de Referência

## Identificação

| Campo | Valor |
|-------|-------|
| **ID** | UC-04 |
| **Nome** | Elaborar Termo de Referência |
| **Ator Principal** | Servidor do setor de compras |
| **Atores Secundários** | Nenhum |
| **Prioridade** | Alta |
| **Origem** | Necessidade de formalizar a especificação da compra |

## Descrição Resumida

O servidor elabora o Termo de Referência com base no ETP, definindo especificações técnicas, critérios de aceitação e obrigações do fornecedor.

## Pré-condições

- ETP já foi aprovado
- Cotação de preços foi realizada

## Pós-condições

### Sucesso
- Termo de Referência gerado e disponível
- TR vinculado ao DFD e ETP originais

### Fracasso
- TR não é gerado
- Sistema registra motivo da falha

## Fluxo Principal (Caminho Feliz)

| Passo | Ator | Ação |
|-------|------|------|
| 1 | Servidor | Acessa funcionalidade "Elaborar Termo de Referência" |
| 2 | Sistema | Exibe lista de ETPs aprovados |
| 3 | Servidor | Seleciona o ETP desejado |
| 4 | Sistema | Carrega dados do ETP (itens, quantidades, preços) |
| 5 | Servidor | Refina especificação técnica (normas, garantias) |
| 6 | Servidor | Define critérios de aceitação do produto/serviço |
| 7 | Servidor | Estabelece obrigações do fornecedor (prazos, entregas) |
| 8 | Servidor | Define sanções para descumprimento |
| 9 | Servidor | Clica em "Gerar TR" |
| 10 | Sistema | Gera documento formatado do Termo de Referência |

## Fluxos Alternativos

### FA-01: Carregar TR existente como modelo
- **Condição de ativação**: Compra similar já foi feita antes
- **A partir do passo**: 5
- **Passos**:
  1. Servidor clica em "Usar modelo existente"
  2. Sistema exibe lista de TRs anteriores
  3. Servidor seleciona um modelo
  4. Sistema carrega especificações do modelo
  5. Servidor ajusta conforme necessidade
- **Retorno ao fluxo principal**: passo 9

## Fluxos de Exceção

### FE-01: ETP sem aprovação
- **Condição**: Servidor tenta selecionar ETP não aprovado
- **Tratamento**:
  1. Sistema oculta ETPs não aprovados da lista
  2. Servidor não vê opção para selecionar
- **Resultado**: TR não pode ser gerado sem ETP aprovado

### FE-02: Especificação inválida
- **Condição**: Servidor tenta salvar sem especificação mínima
- **Tratamento**:
  1. Sistema valida campos obrigatórios
  2. Sistema exibe "Especificação técnica é obrigatória"
  3. Servidor completa e tenta novamente
- **Resultado**: TR não é gerado até correção

## Regras de Negócio Aplicáveis

- RN-01: TR deve referenciar o ETP original
- RN-02: Especificação deve seguir normas técnicas aplicáveis
- RN-03: Prazo de entrega deve ser compatível com mercado
- RN-04: Cotas para ME/EPP devem ser previstas (Lei 123/2006)

## Requisitos Não-Funcionais Relevantes

- RNF-01: TR deve ser exportável em PDF
- RNF-02: TR deve ser versionado (cada edição gera nova versão)
- RNF-03: Alterações devem ser registradas em log de auditoria
