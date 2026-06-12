# 🛠️ Estratégia de Testes e Auditoria — Grupo 02 (ETP)

Este documento explica como o nosso sistema vai validar as informações de cotação de preços e como vamos rastrear as ações dos usuários para garantir que ninguém faça besteira ou fraude no processo de Estudo Técnico Preliminar (ETP). 

Tudo aqui foi baseado nas classes que já temos no nosso diagrama (`Cotacao`, `ETP`, `Fornecedor` e `AnaliseETP`).

---

## 1. Plano de Testes (Validação e Preços Absurdos)

A nossa meta com os testes é não deixar o sistema aceitar dados errados ou valores de cotação que fujam completamente da realidade de mercado (os chamados *outliers*).

### 1.1. Como vamos pegar preços absurdos (Outliers)?
Para evitar que um erro de digitação (como digitar R$ 1000 em vez de R$ 10) estrague a média de preços do ETP, criamos uma trava:
* **A regra:** Sempre que alguém cadastrar uma nova `Cotacao`, o sistema vai olhar para o método `calcularMedia()` da classe `ETP`. 
* **O bloqueio:** Se o preço digitado for **50% maior** ou **50% menor** que a média das outras cotações já guardadas, o método `validar()` vai recusar o salvamento automático e vai exigir que o usuário confirme se o valor está certo mesmo.

### 1.2. Nossos Principais Casos de Teste

| Identificador | O que estamos testando? | O que o usuário digita (Input) | O que o sistema faz (Output) |
| :--- | :--- | :--- | :--- |
| **CT-01** | Preço negativo ou zerado | `preco = -5.00` ou `0.00` | O sistema barra e avisa: *"O valor da cotação precisa ser maior que zero."* |
| **CT-02** | CNPJ com formato errado | `cnpj = "123"` (inválido) | O sistema não deixa avançar com o cadastro do fornecedor e avisa: *"CNPJ inválido."* |
| **CT-03** | Falta de cotações no ETP | Tentar fechar o ETP com só 2 cotações. | O método `gerarETP()` trava e avisa: *"Erro: Você precisa de pelo menos 3 cotações por item."* |
| **CT-04** | Alerta de preço suspeito | Digitar `preco = 500.00` (quando a média é `30.00`) | O sistema joga uma tela de aviso: *"Preço muito fora da média detectado. Deseja confirmar?"* |

---

## 2. Sistema de Auditoria (Histórico de Ações)

Como estamos lidando com um sistema de licitações para a **FACAPE**, precisamos registrar absolutamente tudo o que acontece para auditorias futuras.

### 2.1. O que o nosso Log vai salvar?
Sempre que alguém rodar funções de salvar, atualizar ou gerar o ETP, o sistema vai gravar uma linha de histórico com:
* **Hora exata** da ação.
* **Quem fez** (ID do usuário logado).
* **O que foi feito** (Ex: "Atualizou o preço da cotação X").
* **Os dados antigos e os dados novos** (para sabermos o que foi alterado).

### 2.2. Regras de Controle de Auditoria

| Ação do Usuário | Como o sistema se comporta | Nível de Atenção |
| :--- | :--- | :--- |
| **Cadastrar cotação normal** | Salva a cotação vinculando o `id` dela ao `cnpj` do `Fornecedor`. Segue o fluxo normal. | Baixo |
| **Mudar valor de cotação** | O sistema salva quem mudou, o preço antigo e o preço novo para ficar registrado. | Médio |
| **Escolher a cotação mais cara** | Se o usuário ignorar o menor preço e escolher um mais caro, o sistema obriga ele a escrever uma justificativa no campo `observacao` da classe `AnaliseETP`. | **Alto** |
| **Reprovar a viabilidade** | Se o campo `viabilidade` da classe `AnaliseETP` for marcado como `false`, o sistema exige o motivo detalhado para prestação de contas. | **Alto** |
