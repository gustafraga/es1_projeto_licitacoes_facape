# ADR-002: Avaliação do uso de Event Sourcing e modelo de logs

## Contexto

O sistema necessita armazenar o histórico completo das alterações realizadas nos processos licitatórios, permitindo rastreamento e auditoria das operações. Foi analisada a possibilidade de utilizar o padrão **Event Sourcing**, no qual o estado atual do sistema seria obtido através da reprodução dos eventos registrados.

## Decisão

Foi decidido **não utilizar o padrão Event Sourcing completo**. A solução adotada será baseada em um modelo de **logs imutáveis em formato append-only**, utilizando uma tabela de eventos responsável apenas pelo armazenamento histórico das alterações, sem realizar reconstrução de estados agregados.

## Justificativa

* A reconstrução do estado através de "replay" de eventos não é necessária, pois cada módulo já possui controle do seu estado atual.
* O requisito principal da auditoria é garantir o histórico dos eventos registrados, e não gerar estados derivados a partir desses eventos.
* A abordagem escolhida reduz a complexidade de desenvolvimento e facilita a manutenção do sistema.
* O uso de banco relacional com tabela de eventos atende às necessidades de armazenamento e consulta dos registros.

## Alternativas analisadas

* **Event Sourcing completo (ex.: EventStoreDB)**: não adotado devido ao aumento de complexidade arquitetural e custos adicionais, sem ganhos relevantes para o cenário atual.

## Consequências

* Cada módulo continuará responsável pelo gerenciamento do próprio estado operacional.
* O módulo G09 ficará encarregado apenas do armazenamento do histórico de eventos, sem manter estados agregados.
* Caso futuramente seja necessária uma auditoria baseada em agregações ou projeções, será necessário implementar uma camada específica de leitura.

