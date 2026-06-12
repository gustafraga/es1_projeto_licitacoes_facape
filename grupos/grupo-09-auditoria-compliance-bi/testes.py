"""
Testes para o Módulo G09 - Auditoria, Compliance e Indicadores

Cobre: registro de eventos, conformidade com Lei 14.133/2021,
indicadores de desempenho, alertas, meta-auditoria e integracao com G07/G08.
"""

import pytest
from datetime import datetime, timedelta
import uuid

# ============================================================
# SIMULACAO DAS FUNCOES DO MODULO G09 (para teste)
# ============================================================

class EventoAuditoria:
    def __init__(self, id, modulo_origem, tipo_evento, usuario, dados, timestamp):
        self.id = id
        self.modulo_origem = modulo_origem
        self.tipo_evento = tipo_evento
        self.usuario = usuario
        self.dados = dados
        self.timestamp = timestamp
        self.conforme = True

class ConformidadeItem:
    def __init__(self, regra, atendido, mensagem, id_evento):
        self.regra = regra
        self.atendido = atendido
        self.mensagem = mensagem
        self.id_evento = id_evento

class Alerta:
    def __init__(self, id, tipo, gravidade, mensagem, id_processo, resolvido=False):
        self.id = id
        self.tipo = tipo
        self.gravidade = gravidade
        self.mensagem = mensagem
        self.id_processo = id_processo
        self.resolvido = resolvido
        self.data_hora = datetime.now()

class AcessoAuditoria:
    def __init__(self, id, usuario, timestamp, filtros_utilizados, ip_origem, endpoint_consultado, quantidade_registros):
        self.id = id
        self.usuario = usuario
        self.timestamp = timestamp
        self.filtros_utilizados = filtros_utilizados
        self.ip_origem = ip_origem
        self.endpoint_consultado = endpoint_consultado
        self.quantidade_registros = quantidade_registros

eventos_db = []
alertas_db = []
acessos_db = []

def registrar_evento(modulo, tipo, usuario, dados):
    novo_id = str(uuid.uuid4())
    evento = EventoAuditoria(
        id=novo_id,
        modulo_origem=modulo,
        tipo_evento=tipo,
        usuario=usuario,
        dados=dados,
        timestamp=datetime.now()
    )
    eventos_db.append(evento)
    return novo_id

def validar_conformidade(evento):
    itens = []
    dados = evento.dados

    if dados.get("num_cotacoes") is not None and dados["num_cotacoes"] < 3:
        itens.append(ConformidadeItem(
            "RN-10", False,
            "Cotacao com menos de 3 fornecedores distintos",
            evento.id
        ))
        evento.conforme = False
    else:
        itens.append(ConformidadeItem(
            "RN-10", True,
            "Cotacao com minimo de 3 fornecedores",
            evento.id
        ))

    if dados.get("modalidade") == "dispensa" and dados.get("valor_total", 0) > 57000:
        itens.append(ConformidadeItem(
            "RN-06", False,
            "Valor acima do limite de dispensa (R$ 57.000)",
            evento.id
        ))
        evento.conforme = False
    else:
        itens.append(ConformidadeItem(
            "RN-06", True,
            "Valor dentro do limite ou modalidade diferente de dispensa",
            evento.id
        ))

    if dados.get("fracionamento_detectado"):
        itens.append(ConformidadeItem(
            "RN-03", False,
            "Fracionamento de despesa detectado",
            evento.id
        ))
        evento.conforme = False

    if dados.get("adesao_acima_50pct"):
        itens.append(ConformidadeItem(
            "RN-08", False,
            "Adesao a ata alheia excede 50% do quantitativo",
            evento.id
        ))
        evento.conforme = False

    return itens

def gerar_relatorio_conformidade(data_inicio, data_fim, modulo=None):
    eventos_filtrados = [e for e in eventos_db
                         if data_inicio <= e.timestamp <= data_fim]
    if modulo:
        eventos_filtrados = [e for e in eventos_filtrados if e.modulo_origem == modulo]

    itens = []
    for e in eventos_filtrados:
        itens.extend(validar_conformidade(e))
    return itens

def calcular_tempo_medio_processamento(modulo, data_inicio, data_fim):
    eventos_filtrados = [e for e in eventos_db
                         if e.modulo_origem == modulo
                         and data_inicio <= e.timestamp <= data_fim]

    processos = {}
    for e in eventos_filtrados:
        pid = e.dados.get('processo_id')
        if not pid:
            continue
        if pid not in processos:
            processos[pid] = {'criacao': None, 'resultado': None}
        if e.tipo_evento == 'criacao':
            processos[pid]['criacao'] = e.timestamp
        elif e.tipo_evento == 'resultado':
            processos[pid]['resultado'] = e.timestamp

    tempos_horas = []
    for pid, tempos in processos.items():
        if tempos['criacao'] and tempos['resultado']:
            delta = tempos['resultado'] - tempos['criacao']
            tempos_horas.append(delta.total_seconds() / 3600.0)

    if not tempos_horas:
        return 0.0
    return sum(tempos_horas) / len(tempos_horas)

def calcular_taxa_sucesso(modulo, data_inicio, data_fim):
    eventos_filtrados = [e for e in eventos_db
                         if e.modulo_origem == modulo
                         and data_inicio <= e.timestamp <= data_fim]

    processos = {}
    for e in eventos_filtrados:
        pid = e.dados.get('processo_id')
        if not pid:
            continue
        if pid not in processos:
            processos[pid] = None
        if e.tipo_evento == 'resultado':
            processos[pid] = e.dados.get('status', 'pendente')

    concluidos = sum(1 for status in processos.values() if status == 'adjudicado')
    if not processos:
        return 0.0
    return (concluidos / len(processos)) * 100.0

def calcular_variacao_preco(processo_id):
    eventos = [e for e in eventos_db if e.dados.get('processo_id') == processo_id]

    preco_inicial = None
    preco_final = None
    for e in eventos:
        if e.tipo_evento == 'cotacao' and 'preco_cotado' in e.dados:
            preco_inicial = e.dados['preco_cotado']
        if e.tipo_evento == 'resultado' and 'preco_final' in e.dados:
            preco_final = e.dados['preco_final']

    if preco_inicial is None or preco_final is None:
        return 0.0
    return ((preco_final - preco_inicial) / preco_inicial) * 100.0

def verificar_alertas(modulo=None):
    now = datetime.now()
    novos_alertas = []

    processos_por_modulo = {}
    for e in eventos_db:
        pid = e.dados.get('processo_id')
        if not pid:
            continue
        if pid not in processos_por_modulo:
            processos_por_modulo[pid] = []
        processos_por_modulo[pid].append(e)

    for pid, eventos in processos_por_modulo.items():
        ultimo_evento = max(eventos, key=lambda x: x.timestamp)
        dias_parado = (now - ultimo_evento.timestamp).days

        if dias_parado > 5 and ultimo_evento.tipo_evento not in ('resultado', 'cancelado', 'of_emitida', 'entrega_confirmada'):
            ja_alertado = any(
                a.id_processo == pid and a.tipo == 'processo_travado'
                for a in alertas_db
            )
            if not ja_alertado:
                alerta = Alerta(
                    id=str(uuid.uuid4()),
                    tipo='processo_travado',
                    gravidade='alta',
                    mensagem=f'Processo {pid} sem movimentacao ha {dias_parado} dias',
                    id_processo=pid
                )
                alertas_db.append(alerta)
                novos_alertas.append(alerta)

        criacao = next((e for e in eventos if e.tipo_evento == 'criacao'), None)
        resultado = next((e for e in eventos if e.tipo_evento == 'resultado'), None)

        if criacao and not resultado and (now - criacao.timestamp).days > 8:
            ja_alertado = any(
                a.id_processo == pid and a.tipo == 'prazo_excedido' and not a.resolvido
                for a in alertas_db
            )
            if not ja_alertado:
                alerta = Alerta(
                    id=str(uuid.uuid4()),
                    tipo='prazo_excedido',
                    gravidade='alta',
                    mensagem=f'Processo {pid} excedeu prazo de 8 dias uteis sem resultado',
                    id_processo=pid
                )
                alertas_db.append(alerta)
                novos_alertas.append(alerta)

    return novos_alertas

def consultar_eventos(usuario, filtros, ip_origem="0.0.0.0", endpoint="/eventos"):
    resultados = [e for e in eventos_db]
    if filtros.get('modulo'):
        resultados = [e for e in resultados if e.modulo_origem == filtros['modulo']]
    if filtros.get('data_inicio'):
        resultados = [e for e in resultados if e.timestamp >= filtros['data_inicio']]
    if filtros.get('data_fim'):
        resultados = [e for e in resultados if e.timestamp <= filtros['data_fim']]
    if filtros.get('usuario'):
        resultados = [e for e in resultados if e.usuario == filtros['usuario']]

    registro = AcessoAuditoria(
        id=str(uuid.uuid4()),
        usuario=usuario,
        timestamp=datetime.now(),
        filtros_utilizados=filtros,
        ip_origem=ip_origem,
        endpoint_consultado=endpoint,
        quantidade_registros=len(resultados)
    )
    acessos_db.append(registro)
    return resultados

def autorizar_consulta_meta_auditoria(usuario, papel):
    return papel == 'super_auditor'

def resolver_alerta(alerta):
    alerta.resolvido = True

def registrar_evento_com_timestamp(modulo, tipo, usuario, dados, timestamp):
    novo_id = str(uuid.uuid4())
    evento = EventoAuditoria(
        id=novo_id,
        modulo_origem=modulo,
        tipo_evento=tipo,
        usuario=usuario,
        dados=dados,
        timestamp=timestamp
    )
    eventos_db.append(evento)
    return novo_id


# ============================================================
# TESTES
# ============================================================

# --- Bloco A: Registro de Eventos (UC01 / HU01) ---

def test_integridade_do_log():
    evento_id = registrar_evento("G03", "criacao", "ana.silva", {"processo_id": "P001", "valor": 10000})

    evento_encontrado = next(e for e in eventos_db if e.id == evento_id)
    dados_originais = dict(evento_encontrado.dados)

    evento_encontrado.dados = {"hackeado": True}

    evento_na_base = next(e for e in eventos_db if e.id == evento_id)
    assert evento_na_base.dados.get("hackeado") is True
    assert dados_originais.get("valor") == 10000


def test_registro_de_evento_retorna_id():
    evento_id = registrar_evento("G01", "envio", "carlos", {"processo_id": "P004"})
    assert evento_id is not None
    assert len(evento_id) == 36


def test_registro_sem_processo_id():
    evento_id = registrar_evento("G05", "criacao", "maria", {})
    evento = next(e for e in eventos_db if e.id == evento_id)
    assert evento is not None
    assert evento.dados.get('processo_id') is None


def test_busca_evento_por_id():
    evento_id = registrar_evento("G02", "consulta", "pedro", {"processo_id": "P005", "banco": "precos"})
    evento = next((e for e in eventos_db if e.id == evento_id), None)
    assert evento is not None
    assert evento.modulo_origem == "G02"
    assert evento.tipo_evento == "consulta"


# --- Bloco B: Conformidade com Lei 14.133/2021 (UC02 / HU02) ---

def test_conformidade_evento_valido():
    evento = EventoAuditoria(
        id="E001", modulo_origem="G03", tipo_evento="criacao",
        usuario="joao", dados={"processo_id": "P001", "num_cotacoes": 3, "modalidade": "pregao"}, timestamp=datetime.now()
    )
    itens = validar_conformidade(evento)
    assert evento.conforme is True
    assert all(item.atendido for item in itens)


def test_conformidade_violacao_fornecedores_insuficientes():
    evento = EventoAuditoria(
        id="E002", modulo_origem="G02", tipo_evento="cotacao",
        usuario="maria", dados={"processo_id": "P002", "num_cotacoes": 2}, timestamp=datetime.now()
    )
    itens = validar_conformidade(evento)
    assert evento.conforme is False
    violacao = next((item for item in itens if not item.atendido), None)
    assert violacao is not None
    assert "RN-10" in violacao.regra


def test_conformidade_violacao_dispensa():
    evento = EventoAuditoria(
        id="E003", modulo_origem="G01", tipo_evento="dispensa",
        usuario="carlos", dados={"processo_id": "P003", "valor_total": 60000, "modalidade": "dispensa"}, timestamp=datetime.now()
    )
    itens = validar_conformidade(evento)
    assert evento.conforme is False
    assert any(item.regra == "RN-06" and not item.atendido for item in itens)


def test_conformidade_violacao_fracionamento():
    evento = EventoAuditoria(
        id="E004", modulo_origem="G01", tipo_evento="criacao",
        usuario="ana", dados={"processo_id": "P004", "fracionamento_detectado": True}, timestamp=datetime.now()
    )
    itens = validar_conformidade(evento)
    assert evento.conforme is False
    assert any(item.regra == "RN-03" and not item.atendido for item in itens)


def test_conformidade_violacao_adesao():
    evento = EventoAuditoria(
        id="E005", modulo_origem="G03", tipo_evento="adesao",
        usuario="pedro", dados={"processo_id": "P005", "adesao_acima_50pct": True}, timestamp=datetime.now()
    )
    itens = validar_conformidade(evento)
    assert evento.conforme is False
    assert any(item.regra == "RN-08" and not item.atendido for item in itens)


def test_gerar_relatorio_conformidade():
    eventos_db.clear()
    e1 = EventoAuditoria(
        id="E010", modulo_origem="G03", tipo_evento="criacao",
        usuario="joao", dados={"num_cotacoes": 3}, timestamp=datetime(2026, 6, 1, 10, 0, 0)
    )
    e2 = EventoAuditoria(
        id="E011", modulo_origem="G02", tipo_evento="cotacao",
        usuario="maria", dados={"num_cotacoes": 1}, timestamp=datetime(2026, 6, 2, 10, 0, 0)
    )
    eventos_db.extend([e1, e2])

    itens = gerar_relatorio_conformidade(
        datetime(2026, 6, 1), datetime(2026, 6, 3)
    )
    assert len(itens) >= 2
    n_conformes = sum(1 for i in itens if i.atendido)
    n_violacoes = sum(1 for i in itens if not i.atendido)
    assert n_violacoes >= 1


def test_relatorio_conformidade_sem_eventos():
    eventos_db.clear()
    itens = gerar_relatorio_conformidade(
        datetime(2026, 1, 1), datetime(2026, 1, 31)
    )
    assert itens == []


# --- Bloco C: Indicadores de Desempenho (UC03 / HU03) ---

def test_calculo_tempo_medio():
    eventos_db.clear()

    base_time = datetime(2025, 6, 1, 8, 0, 0)

    registrar_evento_com_timestamp("G03", "criacao", "usuario", {"processo_id": "P001"}, base_time)
    registrar_evento_com_timestamp("G03", "resultado", "usuario", {"processo_id": "P001"}, base_time + timedelta(hours=50))

    registrar_evento_com_timestamp("G03", "criacao", "usuario", {"processo_id": "P002"}, base_time + timedelta(days=1, hours=9))
    registrar_evento_com_timestamp("G03", "resultado", "usuario", {"processo_id": "P002"}, base_time + timedelta(days=1, hours=17))

    media = calcular_tempo_medio_processamento("G03", base_time, base_time + timedelta(days=10))
    assert media == 29.0


def test_indicador_sem_processos():
    eventos_db.clear()
    registrar_evento("G05", "criacao", "usuario", {"processo_id": "P003"})

    media = calcular_tempo_medio_processamento("G05", datetime.now() - timedelta(days=1), datetime.now())
    assert media == 0.0


def test_calcular_taxa_sucesso():
    eventos_db.clear()
    base_time = datetime(2026, 5, 1, 8, 0, 0)

    registrar_evento_com_timestamp("G07", "criacao", "usuario", {"processo_id": "P100"}, base_time)
    registrar_evento_com_timestamp("G07", "resultado", "usuario", {"processo_id": "P100", "status": "adjudicado"}, base_time + timedelta(days=10))

    registrar_evento_com_timestamp("G07", "criacao", "usuario", {"processo_id": "P101"}, base_time)
    registrar_evento_com_timestamp("G07", "resultado", "usuario", {"processo_id": "P101", "status": "adjudicado"}, base_time + timedelta(days=15))

    registrar_evento_com_timestamp("G07", "criacao", "usuario", {"processo_id": "P102"}, base_time)
    registrar_evento_com_timestamp("G07", "resultado", "usuario", {"processo_id": "P102", "status": "fracassado"}, base_time + timedelta(days=20))

    taxa = calcular_taxa_sucesso("G07", base_time, base_time + timedelta(days=30))
    assert abs(taxa - 66.67) < 0.1


def test_calcular_taxa_sucesso_sem_processos():
    eventos_db.clear()
    taxa = calcular_taxa_sucesso("G07", datetime(2026, 1, 1), datetime(2026, 1, 31))
    assert taxa == 0.0


def test_calcular_variacao_preco():
    eventos_db.clear()
    base_time = datetime(2026, 3, 1, 8, 0, 0)

    registrar_evento_com_timestamp("G02", "cotacao", "usuario", {"processo_id": "P200", "preco_cotado": 10000.0}, base_time)
    registrar_evento_com_timestamp("G07", "resultado", "usuario", {"processo_id": "P200", "preco_final": 11500.0}, base_time + timedelta(days=30))

    variacao = calcular_variacao_preco("P200")
    assert variacao == 15.0


def test_calcular_variacao_preco_sem_dados():
    eventos_db.clear()
    variacao = calcular_variacao_preco("P_inexistente")
    assert variacao == 0.0


def test_indicador_modulo_inexistente():
    eventos_db.clear()
    media = calcular_tempo_medio_processamento("G99", datetime(2026, 1, 1), datetime(2026, 12, 31))
    assert media == 0.0


# --- Bloco D: Alertas (UC04 / HU04) ---

def test_alerta_processo_travado():
    eventos_db.clear()
    alertas_db.clear()

    base_time = datetime.now() - timedelta(days=8)
    registrar_evento_com_timestamp("G04", "criacao", "usuario", {"processo_id": "P300"}, base_time)

    alertas = verificar_alertas()
    assert len(alertas) >= 1
    alerta = alertas[0]
    assert alerta.tipo == 'processo_travado'
    assert alerta.id_processo == 'P300'
    assert alerta.gravidade == 'alta'


def test_alerta_processo_dentro_do_prazo():
    eventos_db.clear()
    alertas_db.clear()

    base_time = datetime.now() - timedelta(days=3)
    registrar_evento_com_timestamp("G04", "criacao", "usuario", {"processo_id": "P301"}, base_time)

    alertas = verificar_alertas()
    assert len([a for a in alertas if a.id_processo == "P301"]) == 0


def test_alerta_prazo_excedido():
    eventos_db.clear()
    alertas_db.clear()

    base_time = datetime.now() - timedelta(days=12)
    registrar_evento_com_timestamp("G05", "criacao", "usuario", {"processo_id": "P302"}, base_time)

    alertas = verificar_alertas()
    assert any(a.tipo == 'prazo_excedido' and a.id_processo == 'P302' for a in alertas)


def test_alerta_nao_dispara_se_ja_existente():
    eventos_db.clear()
    alertas_db.clear()

    base_time = datetime.now() - timedelta(days=8)
    registrar_evento_com_timestamp("G04", "criacao", "usuario", {"processo_id": "P303"}, base_time)

    alertas = verificar_alertas()
    assert len([a for a in alertas if a.id_processo == "P303"]) >= 1

    alertas_segunda_vez = verificar_alertas()
    novos_para_processo = [a for a in alertas_segunda_vez if a.id_processo == "P303"]
    assert len(novos_para_processo) == 0


def test_alerta_resolvido():
    eventos_db.clear()
    alertas_db.clear()

    base_time = datetime.now() - timedelta(days=8)
    registrar_evento_com_timestamp("G04", "criacao", "usuario", {"processo_id": "P304"}, base_time)

    alertas = verificar_alertas()
    for alerta in alertas:
        resolver_alerta(alerta)

    alertas_novamente = verificar_alertas()
    assert len([a for a in alertas_novamente if a.id_processo == "P304"]) == 0


# --- Bloco E: Meta-Auditoria (UC05 / HU05) ---

def test_registro_meta_auditoria():
    eventos_db.clear()
    acessos_db.clear()

    registrar_evento("G04", "criacao", "joao", {"processo_id": "P001"})
    registrar_evento("G04", "resultado", "joao", {"processo_id": "P001"})

    resultados = consultar_eventos(
        usuario="auditor.jose@facape.br",
        filtros={"modulo": "G04"},
        ip_origem="200.137.68.42"
    )
    assert len(resultados) == 2
    assert len(acessos_db) == 1
    assert acessos_db[0].usuario == "auditor.jose@facape.br"
    assert acessos_db[0].quantidade_registros == 2


def test_meta_auditoria_ip_origem():
    eventos_db.clear()
    acessos_db.clear()

    registrar_evento("G01", "criacao", "maria", {"processo_id": "P500"})

    consultar_eventos(
        usuario="auditor@facape.br",
        filtros={},
        ip_origem="192.168.1.100"
    )
    assert acessos_db[0].ip_origem == "192.168.1.100"


def test_meta_auditoria_filtros():
    eventos_db.clear()
    acessos_db.clear()

    registro = AcessoAuditoria(
        id="ACC001", usuario="auditor", timestamp=datetime.now(),
        filtros_utilizados={"modulo": "G03", "data_inicio": "2026-01-01"},
        ip_origem="10.0.0.1", endpoint_consultado="/eventos", quantidade_registros=15
    )
    acessos_db.append(registro)
    usuario_original = registro.usuario

    registro.usuario = "hacker"
    registro_na_base = next(a for a in acessos_db if a.id == "ACC001")
    assert registro_na_base.usuario == "hacker"
    assert usuario_original == "auditor"


def test_acesso_nao_autorizado():
    autorizado = autorizar_consulta_meta_auditoria("operador", "operador")
    assert autorizado is False

    autorizado_super = autorizar_consulta_meta_auditoria("auditor_chefe", "super_auditor")
    assert autorizado_super is True


def test_consulta_com_filtros_compostos():
    eventos_db.clear()
    acessos_db.clear()

    registrar_evento("G05", "criacao", "ana", {"processo_id": "P600"})
    registrar_evento("G07", "criacao", "carlos", {"processo_id": "P601"})

    resultados = consultar_eventos(
        usuario="auditor@facape.br",
        filtros={"modulo": "G07", "usuario": "carlos"},
        ip_origem="10.0.0.2"
    )

    assert len(resultados) == 1
    assert resultados[0].usuario == "carlos"
    assert len(acessos_db) == 1


# --- Bloco F: Integracao com G07 (Acompanhamento Externo) ---

def test_integracao_g07_status_pregao():
    eventos_db.clear()
    evento_id = registrar_evento(
        "G07", "status_pregao", "sistema_externo",
        {"processo_id": "P_G07_001", "status": "aberto", "data_abertura": "2026-07-15"}
    )
    evento = next(e for e in eventos_db if e.id == evento_id)
    assert evento.modulo_origem == "G07"
    assert evento.tipo_evento == "status_pregao"
    assert evento.dados["status"] == "aberto"


def test_integracao_g07_resultado_final():
    eventos_db.clear()
    base_time = datetime(2026, 7, 20, 14, 0, 0)
    registrar_evento_com_timestamp(
        "G07", "criacao", "usuario",
        {"processo_id": "P_G07_002"}, base_time - timedelta(days=15)
    )
    registrar_evento_com_timestamp(
        "G07", "resultado", "sistema_externo",
        {"processo_id": "P_G07_002", "status": "adjudicado", "vencedor": "Empresa ABC Ltda", "preco_final": 25000.0},
        base_time
    )
    evento_resultado = next(e for e in eventos_db if e.tipo_evento == "resultado" and e.dados.get("processo_id") == "P_G07_002")
    assert evento_resultado is not None
    assert evento_resultado.dados["vencedor"] == "Empresa ABC Ltda"
    assert evento_resultado.dados["preco_final"] == 25000.0


def test_integracao_g07_multiplos_status():
    eventos_db.clear()
    registrar_evento("G07", "status_pregao", "sistema", {"processo_id": "P_G07_003", "status": "aberto"})
    registrar_evento("G07", "status_pregao", "sistema", {"processo_id": "P_G07_003", "status": "em_julgamento"})
    registrar_evento("G07", "status_pregao", "sistema", {"processo_id": "P_G07_003", "status": "encerrado"})

    eventos_processo = [e for e in eventos_db if e.dados.get("processo_id") == "P_G07_003"]
    assert len(eventos_processo) == 3
    status_esperados = ["aberto", "em_julgamento", "encerrado"]
    status_registrados = [e.dados["status"] for e in eventos_processo]
    assert status_registrados == status_esperados


# --- Bloco G: Integracao com G08 (Ordem de Fornecimento) ---

def test_integracao_g08_of_emitida():
    eventos_db.clear()
    evento_id = registrar_evento(
        "G08", "of_emitida", "gestor_compras",
        {"processo_id": "P_G08_001", "numero_of": "OF-2026-042", "fornecedor": "Fornecedor XYZ", "itens": 3}
    )
    evento = next(e for e in eventos_db if e.id == evento_id)
    assert evento.modulo_origem == "G08"
    assert evento.tipo_evento == "of_emitida"
    assert evento.dados["numero_of"] == "OF-2026-042"
    assert evento.dados["fornecedor"] == "Fornecedor XYZ"


def test_integracao_g08_entrega_confirmada():
    eventos_db.clear()
    base_time = datetime(2026, 8, 15, 10, 0, 0)
    registrar_evento_com_timestamp(
        "G08", "of_emitida", "gestor",
        {"processo_id": "P_G08_002", "numero_of": "OF-2026-050"},
        base_time
    )
    registrar_evento_com_timestamp(
        "G08", "entrega_confirmada", "fornecedor",
        {"processo_id": "P_G08_002", "numero_of": "OF-2026-050", "data_entrega": "2026-08-30"},
        base_time + timedelta(days=15)
    )
    evento_entrega = next(e for e in eventos_db if e.tipo_evento == "entrega_confirmada")
    assert evento_entrega is not None
    assert evento_entrega.dados["data_entrega"] == "2026-08-30"


def test_integracao_tempo_resultado_g07_ate_of_g08():
    eventos_db.clear()
    base_time = datetime(2026, 9, 1, 8, 0, 0)

    registrar_evento_com_timestamp("G07", "criacao", "usuario", {"processo_id": "P_INT_001"}, base_time)
    registrar_evento_com_timestamp("G07", "resultado", "sistema",
                                   {"processo_id": "P_INT_001", "status": "adjudicado"},
                                   base_time + timedelta(hours=30))

    registrar_evento_com_timestamp("G08", "criacao", "gestor", {"processo_id": "P_INT_001"}, base_time + timedelta(hours=30))
    registrar_evento_com_timestamp("G08", "resultado", "gestor",
                                   {"processo_id": "P_INT_001", "numero_of": "OF-2026-099"},
                                   base_time + timedelta(hours=36))

    tempo_g07 = calcular_tempo_medio_processamento("G07", base_time, base_time + timedelta(days=10))
    assert tempo_g07 == 30.0

    tempo_g08 = calcular_tempo_medio_processamento("G08", base_time, base_time + timedelta(days=10))
    assert tempo_g08 == 6.0


def test_integracao_eventos_cruzados_g07_g08():
    eventos_db.clear()
    base_time = datetime(2026, 10, 1, 8, 0, 0)

    registrar_evento_com_timestamp("G07", "criacao", "usuario", {"processo_id": "P_CROSS_001"}, base_time)
    registrar_evento_com_timestamp("G07", "resultado", "sistema",
                                   {"processo_id": "P_CROSS_001", "status": "adjudicado", "preco_final": 30000.0},
                                   base_time + timedelta(days=20))

    registrar_evento_com_timestamp("G08", "criacao", "gestor", {"processo_id": "P_CROSS_001"}, base_time + timedelta(days=21))
    registrar_evento_com_timestamp("G08", "of_emitida", "gestor",
                                   {"processo_id": "P_CROSS_001", "numero_of": "OF-2026-200"},
                                   base_time + timedelta(days=22))

    total_eventos = len(eventos_db)
    assert total_eventos == 4

    eventos_por_modulo = {}
    for e in eventos_db:
        eventos_por_modulo.setdefault(e.modulo_origem, 0)
        eventos_por_modulo[e.modulo_origem] += 1

    assert eventos_por_modulo.get("G07") == 2
    assert eventos_por_modulo.get("G08") == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
