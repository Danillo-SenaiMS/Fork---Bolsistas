import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

GROQ_API_KEY = config('GROQ_API_KEY', default='')
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.3-70b-versatile"


def _get_llm(max_tokens=600):
    return ChatOpenAI(
        model=GROQ_MODEL,
        temperature=0.4,
        max_tokens=max_tokens,
        openai_api_key=GROQ_API_KEY,
        openai_api_base=GROQ_BASE_URL,
    )


def _build_bolsista_context(cadastro):
    formacoes = cadastro.formacoes.order_by('-ano_conclusao')
    formacao_text = ''
    for f in formacoes:
        status = f.get_status_display() if f.status else '---'
        formacao_text += (
            f"- {f.get_tipo_display()} em {f.curso or 'N/A'} "
            f"({status}) - {f.instituicao}"
        )
        if f.ano_conclusao:
            formacao_text += f", conclusão {f.ano_conclusao}"
        if f.area:
            formacao_text += f", área: {f.area}"
        formacao_text += '\n'

    if not formacao_text:
        formacao_text = 'Nenhuma formação cadastrada.\n'

    criterios = []
    if cadastro.participacao_projetos_anos:
        criterios.append(f'{cadastro.participacao_projetos_anos} anos em projetos/pesquisa')
    if cadastro.participacao_congressos:
        criterios.append('Participação em congressos/eventos')
    if cadastro.resumo_anais:
        criterios.append('Resumo publicado em anais')
    if cadastro.artigo_completo_anais:
        criterios.append('Artigo completo em anais')
    if cadastro.artigo_cientifico_nacional:
        criterios.append('Artigo científico nacional')
    if cadastro.artigo_cientifico_internacional:
        criterios.append('Artigo científico internacional')
    if cadastro.livro_patente:
        criterios.append('Livro/patente')
    if cadastro.participacao_minicurso:
        criterios.append('Participação em minicursos')
    if cadastro.treinamento:
        criterios.append('Treinamentos realizados')

    criterios_text = '\n'.join(f'- {c}' for c in criterios) if criterios else 'Nenhum critério adicional.'

    ctx = f"""DADOS DO BOLSISTA

Nome: {cadastro.user.nome_completo}
E-mail: {cadastro.user.email}
Telefone: {cadastro.telefone or 'Nao informado'}
Cidade: {cadastro.cidade or 'Nao informado'}/{cadastro.estado or ''}

FORMAÇÃO ACADÊMICA
{formacao_text}

CRITÉRIOS DE CLASSIFICAÇÃO
{criterios_text}

Pontuação prévia: {cadastro.pontuacao_previa} pontos
"""
    return ctx


def _build_editais_context(editais):
    ctx = ''
    for i, edital in enumerate(editais, 1):
        ctx += f"""
EDITAL {i}: {edital.nome_edital}
Área: {edital.area_estudo}
Plataforma Tecnológica: {edital.plataforma_tecnologica}
Qualificação Mínima: {edital.qualificacao_minima}
Qualificação em: {edital.detalhes_qualificacao_minima or 'Nao informado'}
Conhecimento Desejável: {edital.conhecimento_desejavel or 'Nao informado'}
Vagas: {edital.numero_vagas}
Valor da Bolsa: R$ {float(edital.valor_bolsa):,.2f}
Vigência: {edital.vigencia} dias
Prova Teórica: {edital.conteudo_prova_teorica}
Entrevista: {edital.entrevista}
Status: {edital.get_status_display()}
---
"""
    return ctx


RESUMO_SYSTEM_PROMPT = """Você é um assistente que gera resumos profissionais de candidatos a bolsas de pesquisa.
Seu resumo deve ser CONCISO, com no máximo 3 linhas.
Descreva o perfil acadêmico e pontos de destaque do candidato.
Não invente informações que não estejam nos dados fornecidos.
Responda apenas em português brasileiro."""


def gerar_resumo_bolsista(cadastro) -> dict:
    if not GROQ_API_KEY:
        return {'summary': None, 'error': 'GROQ_API_KEY nao configurada'}

    ctx = _build_bolsista_context(cadastro)
    llm = _get_llm(max_tokens=200)

    messages = [
        SystemMessage(content=RESUMO_SYSTEM_PROMPT),
        HumanMessage(content=f"Gere um resumo conciso do seguinte candidato:\n\n{ctx}"),
    ]

    try:
        response = llm.invoke(messages)
        return {'summary': response.content, 'error': None}
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        return {'summary': None, 'error': str(e)}


ANALISE_SYSTEM_PROMPT = """Você é um especialista em avaliação de candidatos para bolsas de pesquisa do SENAI.
Analise o perfil do candidato comparando com os editais disponíveis.

Responda EXATAMENTE no seguinte formato, sem introduções ou conclusões adicionais:

PONTOS FORTES
- [liste 3-5 pontos fortes do candidato]

PONTOS DE MELHORIA
- [liste 2-3 pontos que o candidato poderia melhorar]

MATCH COM EDITAIS
[Para cada edital, indique o grau de compatibilidade e justificativa resumida]

MELHOR EDITAL: [nome do edital mais compatível]

Responda apenas em português brasileiro. Seja direto e objetivo."""


def analisar_candidato(cadastro, editais) -> dict:
    if not GROQ_API_KEY:
        return {'analise': None, 'error': 'GROQ_API_KEY nao configurada'}

    ctx_bolsista = _build_bolsista_context(cadastro)
    ctx_editais = _build_editais_context(editais)
    llm = _get_llm(max_tokens=800)

    messages = [
        SystemMessage(content=ANALISE_SYSTEM_PROMPT),
        HumanMessage(content=f"""Analise o candidato abaixo em relação aos editais listados:

{ctx_bolsista}

EDITAIS DISPONÍVEIS
{ctx_editais}

Com base nos dados acima, faça a análise completa do candidato.""")
    ]

    try:
        response = llm.invoke(messages)
        return {'analise': response.content, 'error': None}
    except Exception as e:
        logger.error(f"Erro ao analisar candidato: {e}")
        return {'analise': None, 'error': str(e)}
