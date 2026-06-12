# UC-01 — Registrar Demanda de Material/Serviço

## Identificação

| Campo | Valor |
|-------|-------|
| **ID** | UC-01 |
| **Nome** | Registrar Demanda de Material/Serviço |
| **Ator Principal** | Servidor solicitante |
| **Atores Secundários** | Nenhum |
| **Prioridade** | Alta |
| **Origem** | Necessidade das secretarias solicitarem materiais ou serviços |

## Descrição Resumida

O servidor de uma secretaria registra uma demanda por material ou serviço, informando o que precisa, a quantidade e o prazo desejado.

## Pré-condições

- Servidor está autenticado no sistema
- Servidor tem permissão para solicitar materiais

## Pós-condições

### Sucesso
- Demanda registrada com status "Aguardando consolidação"
- Demanda recebe um número de identificação único

### Fracasso
- Demanda não é registrada
- Sistema exibe mensagem de erro

## Fluxo Principal (Caminho Feliz)

| Passo | Ator | Ação |
|-------|------|------|
| 1 | Servidor | Acessa funcionalidade "Registrar Demanda" |
| 2 | Sistema | Exibe formulário de cadastro de demanda |
| 3 | Sistema | Identifica automaticamente a secretaria do servidor autenticado |
| 4 | Servidor | Preenche descrição do material/serviço |
| 5 | Servidor | Informa quantidade e unidade de medida |
| 6 | Servidor | Seleciona prazo desejado para entrega |
| 7 | Servidor | Clica em "Salvar Demanda" |
| 8 | Sistema | Valida os dados informados |
| 9 | Sistema | Gera ID único para a demanda |
| 10 | Sistema | Armazena demanda com status "Aguardando consolidação" |
| 11 | Sistema | Exibe mensagem de confirmação |

## Fluxos Alternativos

### FA-01: Salvar rascunho
- **Condição de ativação**: Servidor não concluiu todos os campos
- **A partir do passo**: 6
- **Passos**:
  1. Servidor clica em "Salvar Rascunho"
  2. Sistema salva dados preenchidos sem validar
  3. Demanda fica com status "Rascunho"
- **Retorno ao fluxo principal**: Servidor pode editar e enviar depois

## Fluxos de Exceção

### FE-01: Campos obrigatórios em branco
- **Condição**: Servidor tenta salvar sem preencher descrição ou quantidade
- **Tratamento**:
  1. Sistema exibe mensagem "Preencha todos os campos obrigatórios"
  2. Sistema marca campos faltantes em vermelho
  3. Servidor preenche e tenta novamente
- **Resultado**: Demanda não é salva até correção

## Regras de Negócio Aplicáveis

- RN-01: Toda demanda deve ter descrição, quantidade e prazo
- RN-02: Quantidade deve ser maior que zero
- RN-03: Prazo não pode ser retroativo
- RN-04: Toda demanda deve estar associada à secretaria do servidor solicitante

## Requisitos Não-Funcionais Relevantes

- RNF-01: Formulário deve carregar em menos de 2 segundos
- RNF-02: ID da demanda deve ser sequencial e único
