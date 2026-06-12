# Backlog do Módulo G09 – Auditoria, Compliance e Indicadores

## HU01 – Registrar evento de auditoria

**Como** módulo de negócio (G01–G08),
**Quero** enviar um evento com dados da operação,
**Para que** ele seja registrado imutavelmente na trilha de auditoria.

### Critérios de Aceitação

* O evento persiste com timestamp, usuário, módulo de origem, tipo de operação e resultado.
* A API retorna um identificador único (UUID).
* Não é possível alterar ou excluir um evento já registrado.

---

## HU02 – Validar conformidade com a Lei 14.133/2021

**Como** auditor de compliance,
**Quero** que cada evento seja automaticamente verificado contra as regras da Lei 14.133/2021,
**Para que** eu identifique rapidamente violações e tome providências.

### Critérios de Aceitação

* Cada evento registrado possui um campo `conforme` (true/false).
* É gerada uma lista de itens de conformidade contendo a regra violada e sua descrição.
* O sistema deve associar cada não conformidade ao respectivo artigo, inciso ou dispositivo legal da Lei 14.133/2021.
* O relatório de conformidade pode ser exportado em PDF.
* O relatório deve apresentar a fundamentação normativa utilizada na validação.

---

## HU03 – Calcular tempo médio de processamento

**Como** gestor de licitações,
**Quero** visualizar o tempo médio entre a criação e o resultado final de um processo,
**Para que** eu identifique gargalos e melhore a eficiência.

### Critérios de Aceitação

* O indicador é atualizado automaticamente a cada novo evento de resultado.
* Permite filtrar por módulo (G01 a G08) e por período.
* O cálculo considera apenas processos concluídos no intervalo.

---

## HU04 – Emitir alerta de processo travado ou prazo ultrapassado

**Como** administrador do sistema,
**Quero** receber alertas quando um processo ficar parado por mais de 5 dias úteis ou quando um prazo regulamentar for excedido,
**Para que** eu possa intervir antes que ocorra uma violação de compliance.

### Critérios de Aceitação

* Alerta disparado automaticamente na primeira verificação após o limite.
* O alerta contém o ID do processo, módulo, tipo de violação e gravidade.
* O alerta é registrado na trilha de auditoria.
* O alerta pode ser resolvido manualmente.

---

## HU05 – Consultar trilha de auditoria

**Como** auditor interno,
**Quero** consultar a trilha de auditoria utilizando filtros por módulo, data e usuário,
**Para que** eu possa realizar análises históricas e investigações de processos.

### Critérios de Aceitação

* A consulta retorna uma lista imutável de eventos.
* O sistema permite combinar múltiplos filtros.
* Os resultados são exibidos em tempo real.
* A visualização é somente leitura.

---

## HU06 – Registrar meta-auditoria de acessos

**Como** responsável por segurança da informação,
**Quero** que cada consulta aos registros de auditoria seja registrada automaticamente,
**Para que** exista rastreabilidade sobre quem acessou informações sensíveis do sistema.

### Critérios de Aceitação

* Cada consulta gera um registro na tabela `acesso_auditoria`.
* O registro contém usuário, timestamp, IP e filtros utilizados.
* O registro é persistido antes da exibição dos resultados da consulta.
* Apenas usuários com papel `super_auditor` podem visualizar os registros de meta-auditoria.
* Os registros são imutáveis após sua criação.
