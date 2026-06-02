# Backlog do Módulo G09 – Auditoria, Compliance e Indicadores

## HU01 – Registrar evento de auditoria
**Como** módulo de negócio (G01–G08),  
**Quero** enviar um evento com dados da operação,  
**Para que** ele seja registrado imutavelmente na trilha de auditoria.

**Critérios de aceitação:**
- O evento persiste com timestamp, usuário, módulo de origem, tipo de operação e resultado.
- A API retorna um identificador único (UUID).
- Não é possível alterar ou excluir um evento já registrado.

---

## HU02 – Validar conformidade com Lei 14.133/2021
**Como** auditor de compliance,  
**Quero** que cada evento seja automaticamente verificado contra as regras da Lei 14.133,  
**Para que** eu identifique rapidamente violações e tome providências.

**Critérios de aceitação:**
- Cada evento registrado possui um campo `conforme` (true/false).
- É gerada uma lista de itens de conformidade com a regra violada e a mensagem.
- O relatório de conformidade pode ser exportado em PDF.

---

## HU03 – Calcular tempo médio de processamento
**Como** gestor de licitações,  
**Quero** visualizar o tempo médio entre a criação e o resultado final de um processo,  
**Para que** eu identifique gargalos e melhore a eficiência.

**Critérios de aceitação:**
- O indicador é atualizado automaticamente a cada novo evento de resultado.
- Permite filtrar por módulo (G01 a G08) e por período.
- O cálculo considera apenas processos concluídos no intervalo.

---

## HU04 – Emitir alerta de processo travado ou prazo ultrapassado
**Como** administrador do sistema,  
**Quero** receber alertas quando um processo ficar parado por mais de 5 dias úteis ou quando um prazo regulamentar for excedido,  
**Para que** eu possa intervir antes que ocorra uma violação de compliance.

**Critérios de aceitação:**
- Alerta disparado automaticamente na primeira verificação após o limite.
- O alerta contém o ID do processo, módulo, tipo de violação e gravidade.
- O alerta é registrado na trilha de auditoria e pode ser resolvido manualmente.

---

## HU05 – Consultar trilha de auditoria com meta-auditoria
**Como** auditor interno,  
**Quero** consultar a trilha de auditoria usando filtros (módulo, data, usuário),  
**Para que** eu possa analisar o histórico de operações.  
**E, como responsável por segurança**, quero que **todas as minhas consultas sejam registradas** em uma meta-auditoria, garantindo rastreabilidade de quem acessou os logs.

**Critérios de aceitação:**
- A consulta retorna uma lista imutável de eventos.
- Cada consulta gera um registro em uma tabela `acesso_auditoria` com usuário, timestamp, filtros e IP.
- Apenas usuários com papel `super_auditor` podem visualizar a meta-auditoria.
