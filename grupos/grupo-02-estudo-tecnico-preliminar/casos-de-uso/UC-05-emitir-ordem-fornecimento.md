# UC-05 — Emitir Ordem de Fornecimento

## Identificação

| Campo | Valor |
|-------|-------|
| **ID** | UC-05 |
| **Nome** | Emitir Ordem de Fornecimento |
| **Ator Principal** | Servidor do setor de compras |
| **Atores Secundários** | Fornecedor vencedor |
| **Prioridade** | Alta |
| **Origem** | Necessidade de formalizar a compra após pregão |

## Descrição Resumida

Após o resultado do pregão externo, o servidor emite a Ordem de Fornecimento para o fornecedor vencedor, especificando itens, quantidades e prazos.

## Pré-condições

- Pregão externo foi concluído na plataforma da Prefeitura
- Resultado do pregão foi registrado no sistema
- Fornecedor vencedor foi identificado

## Pós-condições

### Sucesso
- Ordem de Fornecimento gerada e numerada
- Fornecedor notificado da OF
- Sistema registra status "Aguardando entrega"

### Fracasso
- OF não é emitida
- Erro é registrado para auditoria

## Fluxo Principal (Caminho Feliz)

| Passo | Ator | Ação |
|-------|------|------|
| 1 | Servidor | Acessa funcionalidade "Emitir Ordem de Fornecimento" |
| 2 | Sistema | Exibe lista de pregões concluídos sem OF emitida |
| 3 | Servidor | Seleciona o pregão com resultado |
| 4 | Sistema | Carrega dados: itens, quantidades, fornecedor vencedor |
| 5 | Servidor | Confirma itens e quantidades |
| 6 | Servidor | Define prazo de entrega |
| 7 | Servidor | Especifica local de entrega |
| 8 | Servidor | Clica em "Gerar OF" |
| 9 | Sistema | Gera número único da OF |
| 10 | Sistema | Registra OF com status "Aguardando entrega" |
| 11 | Sistema | Notifica fornecedor (e-mail/sistema) |

## Fluxos Alternativos

### FA-01: Reemitir OF em caso de extravio
- **Condição de ativação**: Fornecedor perdeu ou não recebeu a OF
- **A partir do passo**: 10
- **Passos**:
  1. Servidor acessa OF já emitida
  2. Servidor clica em "Reenviar"
  3. Sistema mantém mesmo número de OF
  4. Sistema envia nova notificação
- **Retorno ao fluxo principal**: Encerramento

## Fluxos de Exceção

### FE-01: Fornecedor não encontrado
- **Condição**: Dados do fornecedor vencedor estão incompletos
- **Tratamento**:
  1. Sistema exibe "Dados do fornecedor incompletos"
  2. Sistema sugere completar cadastro do fornecedor
  3. Servidor completa dados
  4. Servidor tenta emitir novamente
- **Resultado**: OF emitida após correção

### FE-02: Saldo orçamentário insuficiente
- **Condição**: Valor da compra excede saldo disponível
- **Tratamento**:
  1. Sistema exibe "Saldo insuficiente para emissão"
  2. Sistema sugere contato com financeiro
  3. Servidor cancela emissão
- **Resultado**: OF não é emitida

## Regras de Negócio Aplicáveis

- RN-01: OF só pode ser emitida após resultado do pregão
- RN-02: Número da OF deve ser sequencial e único
- RN-03: Prazo de entrega não pode ser inferior a 5 dias úteis
- RN-04: OF deve ser assinada digitalmente pelo comprador

## Requisitos Não-Funcionais Relevantes

- RNF-01: Notificação ao fornecedor deve ser enviada em até 1 minuto
- RNF-02: OF deve ser assinável digitalmente
- RNF-03: Log de emissão deve ser registrado em auditoria
