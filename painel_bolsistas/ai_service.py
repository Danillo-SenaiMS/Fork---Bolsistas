import json
import logging
from decimal import Decimal

from django.conf import settings
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


def _client():
    api_key = getattr(settings, "GOOGLE_API_KEY", None)
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def _gerar_json(client, prompt, max_tokens):
    response = client.models.generate_content(
        model=getattr(settings, "GOOGLE_MODEL", "gemini-1.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.4,
            max_output_tokens=max_tokens,
        ),
    )
    return _parse_json(response.text)


def _perfil_texto(bolsista):
    """Monta uma descrição textual resumida do perfil do candidato."""
    user = bolsista.user
    formacoes = list(bolsista.formacoes.order_by("-ano_conclusao"))
    experiencias = list(bolsista.experiencias.all())

    partes = [
        f"Nome: {user.nome_completo}",
        f"E-mail: {user.email}",
    ]

    if bolsista.telefone:
        partes.append(f"Telefone: {bolsista.telefone}")
    if bolsista.cidade or bolsista.estado:
        partes.append(f"Localização: {bolsista.cidade or ''} / {bolsista.get_estado_display() or ''}".strip(" /"))

    if formacoes:
        partes.append("Formação acadêmica:")
        for f in formacoes:
            linha = f"- {f.get_tipo_display()}"
            if f.curso:
                linha += f" em {f.curso}"
            if f.area:
                linha += f" (área: {f.area})"
            if f.ano_conclusao:
                linha += f", conclusão em {f.ano_conclusao}"
            if f.status:
                linha += f" - {f.get_status_display()}"
            partes.append(linha)
    else:
        partes.append("Formação acadêmica: não informada")

    if experiencias:
        partes.append("Experiência profissional:")
        for e in experiencias:
            partes.append(f"- {e.area_atuacao or 'Área não informada'}: {e.anos_experiencia} ano(s)")

    partes.append("Critérios curriculares:")
    partes.append(f"- Anos em projetos/pesquisa: {bolsista.participacao_projetos_anos}")
    partes.append(f"- Participação em congressos/eventos: {'Sim' if bolsista.participacao_congressos else 'Não'}")
    partes.append(f"- Resumo publicado em anais: {'Sim' if bolsista.resumo_anais else 'Não'}")
    partes.append(f"- Artigo completo em anais: {'Sim' if bolsista.artigo_completo_anais else 'Não'}")
    partes.append(f"- Artigo científico/capítulo nacional: {'Sim' if bolsista.artigo_cientifico_nacional else 'Não'}")
    partes.append(f"- Artigo científico/capítulo internacional: {'Sim' if bolsista.artigo_cientifico_internacional else 'Não'}")
    partes.append(f"- Livro/patente: {'Sim' if bolsista.livro_patente else 'Não'}")
    partes.append(f"- Minicurso: {'Sim' if bolsista.participacao_minicurso else 'Não'}")
    partes.append(f"- Treinamento: {'Sim' if bolsista.treinamento else 'Não'}")

    return "\n".join(partes)


def _editais_texto(editais):
    """Monta uma descrição textual dos editais disponíveis."""
    if not editais:
        return "Nenhum edital cadastrado no momento."

    partes = []
    for edital in editais:
        linhas = [
            f"Edital: {edital.nome_edital or edital.nome_instituto}",
            f"- Instituto: {edital.get_nome_instituto_display()}",
            f"- Modalidade: {edital.get_modalidade_bolsa_display()}",
            f"- Área de estudo: {edital.area_estudo or 'Não informada'}",
            f"- Qualificação mínima: {edital.qualificacao_minima or 'Não informada'}",
            f"- Conhecimento desejável: {edital.conhecimento_desejavel or 'Não informado'}",
            f"- Modalidade de atuação: {edital.get_modalidade_atuacao_display()}",
            f"- Vagas: {edital.numero_vagas}",
            f"- Status: {edital.get_status_display()}",
        ]
        partes.append("\n".join(linhas))
    return "\n\n".join(partes)


def _parse_json(resposta):
    """Tenta extrair JSON de uma resposta que pode vir envolta em markdown."""
    texto = resposta.strip()
    if texto.startswith("```"):
        linhas = texto.splitlines()
        if linhas[0].startswith("```"):
            linhas = linhas[1:]
        if linhas and linhas[-1].startswith("```"):
            linhas = linhas[:-1]
        texto = "\n".join(linhas).strip()
    return json.loads(texto)


def resumir_bolsista(bolsista):
    """Gera um resumo curto e objetivo do candidato."""
    perfil = _perfil_texto(bolsista)
    prompt = (
        "Você é um assistente especializado em recursos humanos e bolsas de pesquisa. "
        "Com base no perfil abaixo, gere um resumo curto, objetivo e em português do Brasil "
        "sobre o candidato. O texto deve ter no máximo 3 linhas e destacar formação, "
        "experiência e pontos fortes.\n\n"
        f"{perfil}\n\n"
        "Responda APENAS com um objeto JSON no formato: {\"resumo\": \"texto aqui\"}"
    )

    client = _client()
    if not client:
        return {"resumo": _resumo_fallback(bolsista)}

    try:
        dados = _gerar_json(client, prompt, max_tokens=250)
        return {"resumo": dados.get("resumo", _resumo_fallback(bolsista))}
    except Exception as e:
        logger.exception("Erro ao gerar resumo com IA: %s", e)
        return {"resumo": _resumo_fallback(bolsista), "erro": str(e)}


def _resumo_fallback(bolsista):
    formacao = bolsista.ultima_formacao
    formacao_str = formacao.get_tipo_display() if formacao else "formação não informada"
    experiencia = f"{bolsista.participacao_projetos_anos} ano(s) em projetos/pesquisa"
    publicacoes = []
    if bolsista.artigo_cientifico_internacional:
        publicacoes.append("artigo internacional")
    elif bolsista.artigo_cientifico_nacional:
        publicacoes.append("artigo nacional")
    elif bolsista.artigo_completo_anais:
        publicacoes.append("artigo em anais")
    elif bolsista.resumo_anais:
        publicacoes.append("resumo em anais")
    if bolsista.livro_patente:
        publicacoes.append("livro/patente")

    partes = [
        f"{bolsista.user.nome_completo} possui {formacao_str} e {experiencia}.",
    ]
    if publicacoes:
        partes.append(f"Possui publicações/produções: {', '.join(publicacoes)}.")
    if bolsista.participacao_congressos:
        partes.append("Participou de congressos, feiras ou eventos na área.")
    return " ".join(partes)


def analisar_bolsista(bolsista, editais):
    """Gera resumo e análise comparativa do candidato frente aos editais, com dados para radar."""
    perfil = _perfil_texto(bolsista)
    editais_texto = _editais_texto(editais)

    prompt = (
        "Você é um assistente especializado em recursos humanos e bolsas de pesquisa. "
        "Analise o perfil do candidato abaixo e compare-o com os editais disponíveis. "
        "Responda APENAS com um objeto JSON no seguinte formato:\n"
        "{\n"
        '  "resumo": "texto breve e objetivo sobre o candidato",\n'
        '  "analise": "texto com a análise do perfil frente aos editais, destacando compatibilidades e gaps",\n'
        '  "radar": [\n'
        '    {"edital": "nome do edital 1", "score": 78},\n'
        '    {"edital": "nome do edital 2", "score": 45}\n'
        '  ]\n'
        "}\n"
        "Regras para o radar:\n"
        "- cada item representa um edital disponível;\n"
        "- o score deve ser um inteiro de 0 a 100 representando o quanto o perfil do candidato se aproxima dos requisitos daquele edital (100 = muito adequado);\n"
        "- se não houver editais, retorne uma lista vazia.\n\n"
        "Perfil do candidato:\n"
        f"{perfil}\n\n"
        "Editais disponíveis:\n"
        f"{editais_texto}"
    )

    client = _client()
    if not client:
        return _analise_fallback(bolsista, editais)

    try:
        dados = _gerar_json(client, prompt, max_tokens=1200)
        return {
            "resumo": dados.get("resumo", _resumo_fallback(bolsista)),
            "analise": dados.get("analise", "Não foi possível gerar a análise comparativa."),
            "radar": _normalizar_radar(dados.get("radar", [])),
        }
    except Exception as e:
        logger.exception("Erro ao analisar candidato com IA: %s", e)
        resultado = _analise_fallback(bolsista, editais)
        resultado["erro"] = str(e)
        return resultado


def _analise_fallback(bolsista, editais):
    resumo = _resumo_fallback(bolsista)
    if not editais:
        return {
            "resumo": resumo,
            "analise": "Não há editais cadastrados para comparação no momento.",
            "radar": [],
        }

    radar = []
    for edital in editais:
        score = _score_heuristico(bolsista, edital)
        radar.append({"edital": edital.nome_edital or str(edital), "score": score})

    return {
        "resumo": resumo,
        "analise": (
            "Análise preliminar baseada nos critérios cadastrados. "
            "Verifique o radar para identificar quais editais possuem maior aderência ao perfil do candidato."
        ),
        "radar": radar,
    }


def _score_heuristico(bolsista, edital):
    """Calcula um score simples quando a IA não está disponível."""
    score = 30  # base

    # Pontuação por formação em relação à qualificação mínima
    formacoes = [f.tipo for f in bolsista.formacoes.all()]
    qualificacao = (edital.qualificacao_minima or "").lower()
    if "doutorado" in qualificacao and "doutorado" in formacoes:
        score += 25
    elif "mestrado" in qualificacao and ("mestrado" in formacoes or "doutorado" in formacoes):
        score += 20
    elif "graduação" in qualificacao and ("graduacao" in formacoes or "mestrado" in formacoes or "doutorado" in formacoes):
        score += 15
    elif "técnico" in qualificacao and ("curso_tecnico" in formacoes or "graduacao" in formacoes):
        score += 10

    # Experiência em projetos
    if bolsista.participacao_projetos_anos >= 2:
        score += 15
    elif bolsista.participacao_projetos_anos >= 1:
        score += 10

    # Critérios curriculares
    if bolsista.artigo_cientifico_internacional:
        score += 10
    elif bolsista.artigo_cientifico_nacional:
        score += 8
    elif bolsista.artigo_completo_anais:
        score += 5

    if bolsista.participacao_congressos:
        score += 5
    if bolsista.livro_patente:
        score += 5
    if bolsista.treinamento:
        score += 5
    if bolsista.participacao_minicurso:
        score += 3

    return min(score, 100)


def _normalizar_radar(radar):
    """Garante que o radar tenha a estrutura esperada e scores válidos."""
    if not isinstance(radar, list):
        return []
    normalizado = []
    for item in radar:
        if not isinstance(item, dict):
            continue
        nome = item.get("edital") or "Edital"
        try:
            score = int(Decimal(str(item.get("score", 0))))
        except Exception:
            score = 0
        score = max(0, min(100, score))
        normalizado.append({"edital": nome, "score": score})
    return normalizado


def _criterios_texto(criterios):
    """Monta uma descricao textual dos criterios de classificacao."""
    partes = []
    for c in criterios:
        linha = (
            f"ID: {c.pk} | Critério: {c.nome} | "
            f"Tipo: {c.get_tipo_criterio_display()} | "
            f"Peso base: {c.peso} pontos"
        )
        if c.peso_maximo > 0:
            linha += f" | Teto máximo: {c.peso_maximo} pontos (critério cumulativo)"
        else:
            linha += " | Binário (atingiu=peso, não atingiu=0)"
        if c.descricao:
            linha += f" | Descrição: {c.descricao}"
        partes.append(linha)
    return "\n".join(partes)


def sugerir_avaliacao(bolsista, criterios):
    """Gera sugestao de pontuacao por criterio com base no perfil do candidato."""
    perfil = _perfil_texto(bolsista)
    criterios_texto = _criterios_texto(criterios)
    criterios_lista = list(criterios)

    prompt = (
        "Você é um assistente especializado em avaliação de candidatos a bolsas de pesquisa. "
        "Com base no perfil do candidato e nos critérios de classificação abaixo, "
        "sugira uma pontuação JUSTA e OBJETIVA para cada critério.\n\n"
        "PERFIL DO CANDIDATO:\n"
        f"{perfil}\n\n"
        "CRITÉRIOS DE CLASSIFICAÇÃO:\n"
        f"{criterios_texto}\n\n"
        "REGRAS PARA PONTUAÇÃO:\n"
        "- Para critérios BINÁRIOS (sem teto máximo): se o candidato atende ao critério, "
        "atribua exatamente o peso base. Caso contrário, atribua 0.\n"
        "- Para critérios CUMULATIVOS (com teto máximo): atribua pontos proporcionais "
        "ao nível de qualificação/experiência do candidato, respeitando o teto.\n"
        "- Exemplo: se o candidato tem 8 anos de projetos e o peso é 5 por ano com teto de 30, "
        "a pontuação seria min(8 × 5, 30) = 30.\n"
        "- Seja 100% imparcial e baseie-se apenas nos dados fornecidos.\n\n"
        "Responda APENAS com um objeto JSON no seguinte formato:\n"
        "{\n"
        '  "resumo": "breve justificativa geral da avaliação sugerida (2-4 linhas)",\n'
        '  "sugestoes": [\n'
        '    {"criterio_id": 1, "pontos": 10.00, "justificativa": "Candidato possui graduação concluída, atende ao critério"},\n'
        '    {"criterio_id": 2, "pontos": 0, "justificativa": "Candidato não possui mestrado"}\n'
        '  ]\n'
        "}\n"
        "IMPORTANTE: use o ID numérico exato de cada critério. Pontos devem ser números decimais com até 2 casas."
    )

    client = _client()
    if not client:
        return _sugerir_avaliacao_fallback(bolsista, criterios_lista)

    try:
        dados = _gerar_json(client, prompt, max_tokens=1500)
        sugestoes_raw = dados.get("sugestoes", [])
        sugestoes = _normalizar_sugestoes(sugestoes_raw, criterios_lista)
        return {
            "resumo": dados.get("resumo", "Sugestão gerada com base no perfil do candidato."),
            "sugestoes": sugestoes,
        }
    except Exception as e:
        logger.exception("Erro ao gerar sugestão de avaliação com IA: %s", e)
        resultado = _sugerir_avaliacao_fallback(bolsista, criterios_lista)
        resultado["erro"] = str(e)
        return resultado


def _sugerir_avaliacao_fallback(bolsista, criterios):
    """Gera sugestao heuristica quando a IA nao esta disponivel."""
    sugestoes = []
    has_graduacao = bolsista.formacoes.filter(tipo='graduacao').exists()
    has_mestrado = bolsista.formacoes.filter(tipo='mestrado').exists()
    has_doutorado = bolsista.formacoes.filter(tipo='doutorado').exists()
    has_pos_doutorado = bolsista.formacoes.filter(tipo='pos_doutorado').exists()

    for criterio in criterios:
        pontos = Decimal('0')
        justificativa = 'Critério não atendido.'

        if criterio.tipo_criterio == 'graduacao' and has_graduacao:
            pontos = criterio.peso
            justificativa = 'Candidato possui graduação concluída.'
        elif criterio.tipo_criterio == 'mestrado' and has_mestrado:
            pontos = criterio.peso
            justificativa = 'Candidato possui mestrado.'
        elif criterio.tipo_criterio == 'doutorado' and (has_doutorado or has_pos_doutorado):
            pontos = criterio.peso
            justificativa = 'Candidato possui doutorado ou pós-doutorado.'
        elif criterio.tipo_criterio == 'projetos_pesquisa':
            anos = bolsista.participacao_projetos_anos
            valor_bruto = Decimal(str(anos)) * criterio.peso
            if criterio.peso_maximo > 0:
                pontos = min(valor_bruto, criterio.peso_maximo)
            else:
                pontos = valor_bruto
            justificativa = f'{anos} ano(s) de experiência em projetos/pesquisa.'
        elif criterio.tipo_criterio == 'congressos' and bolsista.participacao_congressos:
            pontos = criterio.peso
            justificativa = 'Candidato participou de congressos/eventos.'
        elif criterio.tipo_criterio == 'resumo_anais' and bolsista.resumo_anais:
            pontos = criterio.peso
            justificativa = 'Candidato publicou resumo em anais.'
        elif criterio.tipo_criterio == 'artigo_completo_anais' and bolsista.artigo_completo_anais:
            pontos = criterio.peso
            justificativa = 'Candidato publicou artigo completo em anais.'
        elif criterio.tipo_criterio == 'artigo_nacional' and bolsista.artigo_cientifico_nacional:
            pontos = criterio.peso
            justificativa = 'Candidato publicou artigo científico nacional.'
        elif criterio.tipo_criterio == 'artigo_internacional' and bolsista.artigo_cientifico_internacional:
            pontos = criterio.peso
            justificativa = 'Candidato publicou artigo científico internacional.'
        elif criterio.tipo_criterio == 'livro_patente' and bolsista.livro_patente:
            pontos = criterio.peso
            justificativa = 'Candidato possui livro ou patente registrada.'
        elif criterio.tipo_criterio == 'minicurso' and bolsista.participacao_minicurso:
            pontos = criterio.peso
            justificativa = 'Candidato participou de minicurso na área.'
        elif criterio.tipo_criterio == 'treinamento' and bolsista.treinamento:
            pontos = criterio.peso
            justificativa = 'Candidato realizou treinamento na área.'

        sugestoes.append({
            'criterio_id': criterio.pk,
            'criterio_nome': criterio.nome,
            'pontos': pontos,
            'justificativa': justificativa,
        })

    total = sum(s['pontos'] for s in sugestoes)
    return {
        'resumo': (
            f'Sugestão gerada com base nos dados cadastrais do candidato. '
            f'Pontuação total sugerida: {total} pontos. '
            f'Revise cada critério antes de salvar.'
        ),
        'sugestoes': sugestoes,
    }


def _normalizar_sugestoes(sugestoes_raw, criterios):
    """Garante que as sugestoes tenham a estrutura esperada e valores validos."""
    if not isinstance(sugestoes_raw, list):
        return []

    criterios_por_id = {c.pk: c for c in criterios}
    normalizado = []
    for item in sugestoes_raw:
        if not isinstance(item, dict):
            continue
        criterio_id = item.get("criterio_id")
        if criterio_id is None:
            continue
        try:
            criterio_id = int(criterio_id)
        except (ValueError, TypeError):
            continue

        criterio = criterios_por_id.get(criterio_id)
        if not criterio:
            continue

        try:
            pontos = Decimal(str(item.get("pontos", 0)))
        except Exception:
            pontos = Decimal('0')

        pontos = max(Decimal('0'), pontos)
        if criterio.peso_maximo > 0:
            pontos = min(pontos, criterio.peso_maximo)

        justificativa = str(item.get("justificativa", ""))

        normalizado.append({
            "criterio_id": criterio_id,
            "criterio_nome": criterio.nome,
            "pontos": pontos,
            "justificativa": justificativa,
        })

    return normalizado
