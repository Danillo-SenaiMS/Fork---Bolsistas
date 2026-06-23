import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

logger = logging.getLogger(__name__)

GROQ_API_KEY = config('GROQ_API_KEY', default='')
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.3-70b-versatile"


class SummarizeState(TypedDict):
    edital_data: str
    summary: Optional[str]
    error: Optional[str]


def _build_edital_context(edital) -> str:
    cronograma = edital.cronograma.all()
    distribuicoes = edital.distribuicoes.all()

    ctx = f"""
DADOS DO EDITAL

Nome: {edital.nome_edital}
Area de Estudo: {edital.area_estudo}
Detalhes: {edital.detalhes_edital or 'Nao informado'}

INSTITUTO
Nome: {edital.get_nome_instituto_display()}
E-mail: {edital.email_solicitante}
Telefone: {edital.telefone}
Endereco: {edital.endereco}

BOLSA
Modalidade: {edital.get_modalidade_bolsa_display()}
Valor Total: R$ {float(edital.valor_total_bolsa):,.2f}
Valor da Bolsa: R$ {float(edital.valor_bolsa):,.2f}
Modalidade de Atuacao: {edital.get_modalidade_atuacao_display()}
Plataforma Tecnologica: {edital.plataforma_tecnologica}
Vigencia: {edital.vigencia} dias
Endereco de Atuacao: {edital.endereco_atuacao or 'Nao informado'}
Numero de Vagas: {edital.numero_vagas}
"""

    if distribuicoes:
        ctx += "\nDISTRIBUICAO DE BOLSISTAS\n"
        for d in distribuicoes:
            ctx += f"- {d.quantidade}x {d.experiencia}: R$ {float(d.valor_unitario):,.2f} cada (subtotal: R$ {float(d.subtotal):,.2f})\n"
        ctx += f"Total Distribuido: R$ {float(edital.total_distribuido):,.2f}\n"

    ctx += f"""
REQUISITOS
Qualificacao Minima: {edital.qualificacao_minima}
Qualificacao Minima em: {edital.detalhes_qualificacao_minima or 'Nao informado'}
Conhecimento Desejavel: {edital.conhecimento_desejavel or 'Nao informado'}

AVALIACAO
Conteudo da Prova Teorica: {edital.conteudo_prova_teorica}
Entrevista: {edital.entrevista}
Criterios de Desempate: {edital.criterios_desempate}
"""

    if cronograma:
        ctx += "\nCRONOGRAMA\n"
        for e in cronograma:
            ctx += f"- {e.get_evento_display()}: {e.data_referencia}"
            if e.observacao:
                ctx += f" ({e.observacao})"
            ctx += "\n"

    ctx += f"\nSTATUS: {edital.get_status_display()}\n"
    return ctx


SYSTEM_PROMPT = """Voce e um assistente que resume editais de bolsas de pesquisa do SENAI.
Seu resumo deve ser PRECISO, DIRETO e OBJETIVO.
Nao invente dados que nao estejam no edital.
Estruture o resumo em topicos curtos, um por linha.
Responda apenas em portugues brasileiro.

Formato obrigatorio:

**Resumo do Edital**

**Objetivo:** 1-2 linhas sobre o que e o edital
**Bolsa:** valor e modalidade
**Requisitos:** qualificacao minima
**Vagas:** quantidade e distribuicao (se houver)
**Etapas:** principais eventos do cronograma
**Instituto:** nome e contato
**Vigencia:** prazo da bolsa"""


def _get_llm():
    return ChatOpenAI(
        model=GROQ_MODEL,
        temperature=0.3,
        max_tokens=600,
        openai_api_key=GROQ_API_KEY,
        openai_api_base=GROQ_BASE_URL,
    )


def summarize_edital(edital) -> dict:
    ctx = _build_edital_context(edital)
    llm = _get_llm()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resuma o seguinte edital de forma precisa e objetiva:\n\n{ctx}"),
    ]

    try:
        response = llm.invoke(messages)
        return {"summary": response.content, "error": None}
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        return {"summary": None, "error": str(e)}


AVALIAR_SYSTEM_PROMPT = """Voce e um assistente que avalia a compatibilidade de candidatos com editais de bolsas de pesquisa do SENAI.
Analise o perfil do candidato comparando com os requisitos do edital.
Seja PRECISO, DIRETO e OBJETIVO.
Nao invente dados que nao estejam no contexto fornecido.
Responda apenas em portugues brasileiro.

Formato de resposta obrigatorio (exatamente assim, sem texto adicional):

COMPATIBILIDADE: <percentual entre 0 e 100>
NOTA: <nota de 0.00 a 10.00 baseada na formacao, experiencia e aderencia aos requisitos>
RESUMO: <2 a 3 frases curtas e objetivas resumindo os pontos fortes e fracos do candidato para esta vaga>"""


def _build_candidato_context(cadastro, aplicacao) -> str:
    formacoes = cadastro.formacoes.all()
    ctx = f"""
PERFIL DO CANDIDATO

Nome: {cadastro.user.nome_completo}
Data de Nascimento: {cadastro.data_nascimento.strftime('%d/%m/%Y') if cadastro.data_nascimento else 'Nao informado'}
Cidade/Estado: {cadastro.cidade}/{cadastro.estado}

FORMACAO ACADEMICA
"""
    for f in formacoes:
        status = f.get_status_display() if f.status else ''
        ctx += f"- {f.get_tipo_display()}{' (' + status + ')' if status else ''}"
        if f.area:
            ctx += f" | Area: {f.area}"
        if f.curso:
            ctx += f" | Curso: {f.curso}"
        if f.ano_conclusao:
            ctx += f" | Conclusao: {f.ano_conclusao}"
        ctx += "\n"

    if not formacoes:
        ctx += "Nenhuma formacao cadastrada.\n"

    ctx += f"""
EXPERIENCIA E PRODUCAO
Anos em projetos/pesquisa: {cadastro.participacao_projetos_anos}
Participacao em congressos: {'Sim' if cadastro.participacao_congressos else 'Nao'}
Resumo em anais: {'Sim' if cadastro.resumo_anais else 'Nao'}
Artigo completo em anais: {'Sim' if cadastro.artigo_completo_anais else 'Nao'}
Artigo nacional: {'Sim' if cadastro.artigo_cientifico_nacional else 'Nao'}
Artigo internacional: {'Sim' if cadastro.artigo_cientifico_internacional else 'Nao'}
Livro ou patente: {'Sim' if cadastro.livro_patente else 'Nao'}
Minicurso (ate 4h): {'Sim' if cadastro.participacao_minicurso else 'Nao'}
Treinamento (acima de 4h): {'Sim' if cadastro.treinamento else 'Nao'}
Pontuacao previa: {cadastro.pontuacao_previa}

APLICACAO
Status: {aplicacao.get_status_display()}
Data: {aplicacao.data_aplicacao.strftime('%d/%m/%Y')}
"""
    return ctx


def avaliar_candidato(edital, cadastro, aplicacao) -> dict:
    edital_ctx = _build_edital_context(edital)
    candidato_ctx = _build_candidato_context(cadastro, aplicacao)
    llm = _get_llm()

    full_context = f"{edital_ctx}\n\n{candidato_ctx}"

    messages = [
        SystemMessage(content=AVALIAR_SYSTEM_PROMPT),
        HumanMessage(content=f"Avalie a compatibilidade deste candidato com o edital abaixo:\n\n{full_context}"),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        compatibilidade = None
        nota = None
        resumo = None
        for line in content.split('\n'):
            upper = line.upper()
            if upper.startswith('COMPATIBILIDADE:'):
                try:
                    compatibilidade = int(''.join(c for c in line.split(':', 1)[1] if c.isdigit()))
                except ValueError:
                    compatibilidade = None
            elif upper.startswith('NOTA:'):
                try:
                    nota = float(line.split(':', 1)[1].strip().replace(',', '.'))
                    nota = min(max(nota, 0), 10)
                except (ValueError, IndexError):
                    nota = None
            elif upper.startswith('RESUMO:'):
                resumo = line.split(':', 1)[1].strip()

        if compatibilidade is None or resumo is None:
            return {"compatibilidade": None, "nota": nota, "resumo": content, "error": None}

        return {"compatibilidade": compatibilidade, "nota": nota, "resumo": resumo, "error": None}
    except Exception as e:
        logger.error(f"Erro ao avaliar candidato: {e}")
        return {"compatibilidade": None, "nota": None, "resumo": None, "error": str(e)}


LISTA_SUMMARY_SYSTEM_PROMPT = """Voce e um assistente que resume o panorama geral de editais de bolsas de pesquisa do SENAI.
Com base nos dados estatisticos fornecidos, produza um resumo conciso, direto e objetivo em linguagem natural.
Nao invente numeros que nao estejam nos dados. Arredonde valores monetarios para facilitar a leitura.
Responda apenas em portugues brasileiro.

Formato obrigatorio (use topicos curtos, um por linha):

**Panorama Geral de Editais**

**Resumo:** 1-2 frases destacando o numero total de editais abertos e o destaque do periodo.
**Editais Abertos:** quantidade total de editais com status aberto.
**Por Instituicao:** quantidade de editais por instituto (liste cada um).
**Valores:** valor total disponivel em bolsas e valor medio da bolsa.
**Por Periodo:** distribuicao da quantidade de editais abertos por ano de criacao."""


def summarize_editais_lista(stats: dict) -> dict:
    ctx_parts = [
        f"Numero total de editais abertos: {stats['total_abertos']}",
        f"Numero total de editais (todos os status): {stats['total_geral']}",
    ]
    if stats['por_instituicao']:
        ctx_parts.append("Editais abertos por instituicao:")
        for instituto, qtd in stats['por_instituicao'].items():
            ctx_parts.append(f"- {instituto}: {qtd}")
    else:
        ctx_parts.append("Nenhum edital aberto por instituicao.")
    ctx_parts.append(f"Valor total das bolsas (editais abertos): R$ {stats['valor_total']:,.2f}")
    ctx_parts.append(f"Valor medio da bolsa (editais abertos): R$ {stats['valor_medio']:,.2f}")
    if stats['por_periodo']:
        ctx_parts.append("Editais abertos por periodo (ano de criacao):")
        for ano, qtd in stats['por_periodo'].items():
            ctx_parts.append(f"- {ano}: {qtd}")
    else:
        ctx_parts.append("Nenhum edital aberto por periodo.")
    ctx = "\n".join(ctx_parts)

    llm = _get_llm()
    messages = [
        SystemMessage(content=LISTA_SUMMARY_SYSTEM_PROMPT),
        HumanMessage(content=f"Resuma o panorama de editais a partir dos dados abaixo:\n\n{ctx}"),
    ]
    try:
        response = llm.invoke(messages)
        return {"summary": response.content, "error": None}
    except Exception as e:
        logger.error(f"Erro ao gerar resumo da lista de editais: {e}")
        return {"summary": None, "error": str(e)}


def build_summarize_graph():
    workflow = StateGraph(SummarizeState)

    def summarize_node(state: SummarizeState) -> SummarizeState:
        llm = _get_llm()
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Resuma o seguinte edital de forma precisa e objetiva:\n\n{state['edital_data']}"),
        ]
        try:
            response = llm.invoke(messages)
            state["summary"] = response.content
        except Exception as e:
            state["error"] = str(e)
        return state

    workflow.add_node("summarize", summarize_node)
    workflow.set_entry_point("summarize")
    workflow.add_edge("summarize", END)

    return workflow.compile()
