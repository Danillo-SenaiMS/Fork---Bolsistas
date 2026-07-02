from django.http import FileResponse, Http404, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.db import connection
from pathlib import Path

from accounts.models import DocumentoExterno
from cadastro.models import CadastroBolsista, AnexoComprobatorio, ExperienciaProfissional
from .mixins import GROUP_MANAGER


def health_check(request):
    """Endpoint simples para health checks do load balancer/monitoramento."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"status": "ok"}, status=200)
    except Exception as exc:
        return JsonResponse({"status": "error", "detail": str(exc)}, status=503)

PASTAS_RESTRITAS = {
    'curriculos': CadastroBolsista,
    'fotos': CadastroBolsista,
    'anexos': AnexoComprobatorio,
    'experiencias': ExperienciaProfissional,
}


def _verificar_dono_arquivo(request, relative):
    """Verifica se o usuario autenticado eh dono do arquivo em pastas restritas."""
    for prefix, model in PASTAS_RESTRITAS.items():
        if not relative.startswith(prefix + '/'):
            continue
        if model == CadastroBolsista:
            cadastro = CadastroBolsista.objects.filter(user=request.user).first()
            if cadastro:
                campo_arquivo = 'curriculo' if prefix == 'curriculos' else 'foto'
                arquivo_campo = getattr(cadastro, campo_arquivo, None)
                if arquivo_campo and arquivo_campo.name == relative:
                    return True
            return False
        else:
            obj = model.objects.filter(anexo=relative).first()
            if obj and hasattr(obj, 'bolsista') and obj.bolsista.user == request.user:
                return True
            return False
    return False


def media_protegida(request, path):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Acesso negado')

    media_root = Path(settings.MEDIA_ROOT).resolve()
    arquivo_path = (media_root / path).resolve()

    if not str(arquivo_path).startswith(str(media_root)):
        return HttpResponseForbidden('Acesso negado')

    if not arquivo_path.exists() or not arquivo_path.is_file():
        raise Http404('Arquivo não encontrado')

    if request.user.is_superuser or request.user.groups.filter(name=GROUP_MANAGER).exists():
        return FileResponse(open(arquivo_path, 'rb'))

    relative = path.replace('\\', '/')
    if relative.startswith('documentos/'):
        doc = DocumentoExterno.objects.filter(arquivo=relative).first()
        if doc and doc.user == request.user:
            return FileResponse(open(arquivo_path, 'rb'))
        return HttpResponseForbidden('Acesso negado')

    if _verificar_dono_arquivo(request, relative):
        return FileResponse(open(arquivo_path, 'rb'))

    return HttpResponseForbidden('Acesso negado')
