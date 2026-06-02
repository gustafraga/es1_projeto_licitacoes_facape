# Casos de Uso – Módulo G09

| ID | Nome | Ator principal | Pré‑condição | Fluxo principal | Pós‑condição |
|----|------|----------------|--------------|----------------|---------------|
| UC01 | Registrar Evento de Auditoria | Módulos G01–G08 | Evento ocorreu no sistema | 1. Módulo origem envia evento via API. 2. Sistema valida formato. 3. Persiste log imutável (timestamp, usuário, ação, resultado). 4. Retorna ID do evento. | Evento registrado na trilha |
| UC02 | Gerar Relatório de Conformidade | Gestor de Compliance | Período informado | 1. Solicita relatório. 2. Consulta eventos do período. 3. Aplica regras da Lei 14.133/2021. 4. Gera relatório em PDF/CSV. | Relatório disponível |
| UC03 | Calcular Indicadores de Desempenho | Administrador | Eventos registrados | 1. Rotina periódica (diária). 2. Calcula tempo médio, taxa de sucesso, variação de preços. 3. Armazena indicadores. | Indicadores atualizados |
| UC04 | Emitir Alerta Automático | Sistema de Auditoria | Condição de alerta detectada | 1. A cada novo evento, avalia regras. 2. Dispara alerta (e-mail/Slack). 3. Registra alerta na trilha. | Alerta notificado |
| UC05 | Consultar Trilha de Auditoria | Auditor interno | Usuário autenticado | 1. Aplica filtros (módulo, data). 2. Retorna lista imutável. 3. Registra consulta na meta‑auditoria. | Log de acesso registrado |
