# Plano de Testes — Módulo G09 (Auditoria, Compliance e Indicadores)

## 1. Objetivos e Escopo

Este plano descreve a estratégia de testes para o módulo G09, responsável por registrar a trilha de auditoria centralizada (eventos de G01–G08), validar conformidade com a Lei 14.133/2021, calcular indicadores de desempenho e emitir alertas.

**Objetivos do teste:**
- Garantir integridade e imutabilidade dos logs de auditoria
- Verificar a correta validação de conformidade legal
- Validar o cálculo preciso dos indicadores de negócio
- Assegurar o disparo correto de alertas
- Confirmar a rastreabilidade de acessos (meta-auditoria)
- Validar a integração com os módulos vizinhos G07 e G08

**Fora do escopo de teste:**
- Testes de desempenho e carga (não exigidos para esta fase)
- Testes de segurança de infraestrutura
- Testes de integração com sistemas externos (PNCP, Banco de Preços)

---

## 2. Estratégia de Testes

### 2.1 Pirâmide de Testes

| Nível | Quantidade | Foco |
|-------|-----------|------|
| **Unitário** | Alta | Funções isoladas: registro de evento, cálculo de indicadores, validação de conformidade, disparo de alertas |
| **Integração** | Média | Fluxo de eventos vindos de G07 e G08, persistência simulada, meta-auditoria |
| **Sistema** | Baixa | Pipeline completo: evento → registro → conformidade → indicador → alerta → meta-auditoria |
| **Aceite** | Por HU | Cada história de usuário validada contra seus critérios de aceitação |

### 2.2 Critérios de Entrada e Saída

**Entrada (quando começar a testar):**
- Funções do módulo implementadas (simulação em memória)
- Dados de teste preparados (eventos, módulos, timestamps)
- Ambiente pytest configurado

**Saída (quando o teste está concluído):**
- 100% dos casos de teste executados
- 0 falhas em testes unitários e de integração
- Evidências de execução documentadas (prints, logs)

### 2.3 Ambiente de Testes

| Parâmetro | Valor |
|-----------|-------|
| Linguagem | Python 3 |
| Framework | pytest |
| Persistência | Simulada em memória (listas e dicionários) |
| Dependências externas | Nenhuma (self-contained) |
| Execução | `pytest testes.py -v` |

---

## 3. Riscos de Qualidade Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Log de auditoria permitir alteração indevida | Baixa | Crítico | Teste de imutabilidade com verificação de exceção |
| Cálculo incorreto de indicadores (divisão por zero, dados ausentes) | Média | Alto | Testes de borda: 0 processos, dados faltantes |
| Alertas não dispararem no prazo correto | Média | Alto | Testes com timestamps controlados e verificação de trigger |
| Meta-auditoria não registrar consultas | Alta | Médio | Teste que força consulta e verifica registro automático |
| Integração com G07/G08 quebrar por formato de dados incompatível | Média | Alto | Testes de contrato com payloads simulados dos módulos vizinhos |

---

## 4. Casos de Teste

### Bloco A: Registro de Eventos de Auditoria (UC01 / HU01)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-A01 | Registrar evento com dados válidos | Funcional | modulo="G03", tipo="criacao", usuario="ana", dados={"processo_id":"P001"} | Retorna UUID de 36 caracteres |
| CT-A02 | Registrar evento sem processo_id | Negativo | dados={} | Registra normalmente (campo opcional) |
| CT-A03 | Tentar alterar evento após registro (imutabilidade) | Negativo | evento_registrado.dados = {...} | Levanta exceção (AttributeError) |
| CT-A04 | Buscar evento por ID após registro | Funcional | ID retornado por registrar_evento() | Dados originais preservados |

### Bloco B: Conformidade com Lei 14.133/2021 (UC02 / HU02)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-B01 | Evento em conformidade marcado como true | Funcional | Evento com dados completos e válidos | evento.conforme == True |
| CT-B02 | Validar regra: processo sem cotação mínima de 3 fornecedores | Negativo | Evento com campo "num_cotacoes": 2 | Item de conformidade retorna não atendido |
| CT-B03 | Validar regra: valor acima do limite de dispensa (R$ 57.000) | Funcional | Evento com valor total = 60000, modalidade = "dispensa" | Retorna violação |
| CT-B04 | Gerar relatório de conformidade com múltiplos eventos | Funcional | 3 eventos, 1 violação | Relatório lista 3 itens, 1 não conforme |
| CT-B05 | Gerar relatório sem eventos no período | Borda | Período sem nenhum evento registrado | Relatório vazio, sem erros |

### Bloco C: Cálculo de Indicadores (UC03 / HU03)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-C01 | Tempo médio com 2 processos completos (50h e 8h) | Funcional | Eventos com timestamps conhecidos | Média = 29.0 horas |
| CT-C02 | Tempo médio sem processos concluídos | Borda | Apenas criação, sem resultado | Retorna 0.0 |
| CT-C03 | Taxa de sucesso: 3 processos, 2 com resultado "adjudicado" | Funcional | 3 processos, status variados | Taxa = 66.67% |
| CT-C04 | Taxa de sucesso sem processos | Borda | Nenhum evento | Retorna 0.0 |
| CT-C05 | Variação de preço: valor cotado vs. valor final | Funcional | Dados com precos_iniciais e precos_finais | Percentual calculado corretamente |
| CT-C06 | Filtrar indicador por módulo inexistente | Borda | modulo="G99" | Retorna 0.0 |

### Bloco D: Emissão de Alertas (UC04 / HU04)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-D01 | Alerta de processo travado (5+ dias úteis sem eventos) | Funcional | Último evento há 6 dias úteis | Alerta disparado com tipo="processo_travado" |
| CT-D02 | Processo dentro do prazo (3 dias) | Funcional | Último evento há 3 dias úteis | Nenhum alerta gerado |
| CT-D03 | Prazo de pregão ultrapassado (>8 dias úteis) | Funcional | Evento com criacao > 8 dias e sem resultado | Alerta disparado com tipo="prazo_excedido" |
| CT-D04 | Alerta resolvido não re-dispara | Funcional | Alerta já resolvido, nova verificação | Nenhum novo alerta para mesmo processo |

### Bloco E: Meta-Auditoria (UC05 / HU05)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-E01 | Registrar consulta à trilha de auditoria | Funcional | usuario="auditor", modulo="G04", filtros | Registro criado em acesso_auditoria |
| CT-E02 | Meta-auditoria registra IP de origem | Funcional | ip="200.137.68.42" | Campo ip_origem preenchido |
| CT-E03 | Acesso não autorizado (sem papel super_auditor) | Negativo | usuario com papel "operador" | Acesso negado |
| CT-E04 | Registro de meta-auditoria é imutável | Funcional | Tentativa de alterar registro | Exceção lançada |

### Bloco F: Integração com G07 (Acompanhamento Externo)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-F01 | Receber evento de status de pregão (G07) | Integração | modulo="G07", tipo="status_pregão", dados={"status":"aberto","processo_id":"P010"} | Evento registrado com modulo_origem="G07" |
| CT-F02 | Receber evento de resultado final (G07) | Integração | modulo="G07", tipo="resultado", dados={"processo_id":"P010","vencedor":"Empresa X","valor":50000} | Evento registrado, indicador de tempo atualizado |
| CT-F03 | Múltiplos eventos do mesmo processo (G07) | Integração | 3 eventos de status para mesmo processo_id | Todos registrados, timeline preservada |

### Bloco G: Integração com G08 (Ordem de Fornecimento)

| ID | Caso de Teste | Tipo | Entrada | Resultado Esperado |
|----|--------------|------|---------|-------------------|
| CT-G01 | Receber evento de OF emitida (G08) | Integração | modulo="G08", tipo="of_emitida", dados={"processo_id":"P011","numero_of":"OF-2026-001"} | Evento registrado na trilha |
| CT-G02 | Receber evento de confirmação de recebimento (G08) | Integração | modulo="G08", tipo="entrega_confirmada", dados={"processo_id":"P011"} | Evento registrado |
| CT-G03 | Calcular tempo entre resultado do pregão e emissão da OF | Integração | Eventos G07(resultado) e G08(of_emitida) | Tempo calculado corretamente (em horas) |

---

## 5. Matriz de Rastreabilidade

| Caso de Teste | User Story | Regra de Negócio | Nível |
|---------------|-----------|-----------------|-------|
| CT-A01–A04 | HU01 | — | Unitário |
| CT-B01–B05 | HU02 | RN-01, RN-10 | Unitário |
| CT-C01–C06 | HU03 | — | Unitário |
| CT-D01–D04 | HU04 | RN-07 | Unitário |
| CT-E01–E04 | HU05 | — | Integração |
| CT-F01–F03 | HU01 (integração) | — | Integração |
| CT-G01–G03 | HU01, HU03 (integração) | — | Integração |

---

## 6. Implementação Automatizada

Os casos de teste marcados como "Unitário" e "Integração" são implementados como funções pytest no arquivo `testes.py`. Cada função segue o padrão:

```python
def test_<descricao>():
    # Arrange: preparar dados
    # Act: executar função
    # Assert: verificar resultado
```

**Comando de execução:**
```bash
pytest testes.py -v
```

---

## 7. Evidências de Execução

As evidências são geradas automaticamente pelo pytest no formato:
```
testes.py::test_integridade_do_log PASSED
testes.py::test_calculo_tempo_medio PASSED
...
======= X passed in Y.Zs =======
```

O relatório completo de testes pode ser exportado com:
```bash
pytest testes.py -v --tb=long > resultado-testes.txt
```
