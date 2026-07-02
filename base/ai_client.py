import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def get_provider():
    """Retorna o provedor de IA ativo ('openai', 'google' ou None)."""
    provider = getattr(settings, "IA_PROVIDER", None)
    if provider:
        return provider
    if getattr(settings, "OPENAI_API_KEY", None):
        return "openai"
    if getattr(settings, "GOOGLE_API_KEY", None):
        return "google"
    return None


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


def _openai_json(prompt, max_tokens):
    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.4,
        max_tokens=max_tokens,
    )
    return _parse_json(response.choices[0].message.content)


def _google_json(prompt, max_tokens):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    model = getattr(settings, "GOOGLE_MODEL", "gemini-2.0-flash")
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.4,
            max_output_tokens=max_tokens,
        ),
    )
    return _parse_json(response.text)


def gerar_json(prompt, max_tokens):
    """Gera uma resposta em JSON usando o provedor configurado."""
    provider = get_provider()
    if provider == "openai":
        return _openai_json(prompt, max_tokens)
    if provider == "google":
        return _google_json(prompt, max_tokens)
    raise RuntimeError("Nenhum provedor de IA configurado.")
