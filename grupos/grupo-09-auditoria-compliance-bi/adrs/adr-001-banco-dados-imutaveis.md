# ADR-001: Definição do banco de dados para armazenamento de logs imutáveis

## Contexto

O módulo G09 é responsável por armazenar os eventos enviados pelos módulos G01 até G08, garantindo que as informações permaneçam íntegras, rastreáveis e disponíveis para auditoria, atendendo aos requisitos de não-repúdio definidos pela Lei 14.133/2021.

## Decisão

Foi definido o uso do **PostgreSQL** para persistência dos registros de auditoria, utilizando as seguintes abordagens:

* Tabela `evento_auditoria` estruturada no modelo **append-only**, utilizando:

  * `REVOKE UPDATE, DELETE ON evento_auditoria FROM app_user;`
  * Trigger de proteção para bloquear tentativas de alteração ou remoção dos registros.
* Identificadores primários utilizando `UUID` gerados pelo sistema.
* Particionamento dos dados realizado mensalmente com base no campo `timestamp`, visando melhorar o desempenho das consultas.
* Criação de índice composto em `(modulo_origem, timestamp)` para otimizar buscas recorrentes.

## Alternativas analisadas

* **Amazon QLDB**: descartado devido à dependência de fornecedor e aos custos envolvidos.
* **Blockchain (Hyperledger)**: considerada uma solução excessiva para a necessidade atual, adicionando complexidade desnecessária.
* **Arquivos de logs rotacionados**: não adotado por apresentar limitações em consultas, organização e garantia de integridade dos dados.

## Consequências

* Será necessário executar processos de arquivamento e gerenciamento de partições antigas, mantendo os dados pelo período mínimo de 5 anos conforme legislação.
* A realização de backups periódicos da tabela de auditoria permanece obrigatória.
* Consultas analíticas de grande volume podem demandar otimizações adicionais de índices.
