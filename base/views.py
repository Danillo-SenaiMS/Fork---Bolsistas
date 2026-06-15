from django.http import FileResponse, Http404, HttpResponseForbidden
from django.conf import settings
from pathlib import Path


def media_protegida(request, path):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Acesso negado')

    arquivo_path = Path(settings.MEDIA_ROOT) / path

    if not arquivo_path.exists() or not arquivo_path.is_file():
        raise Http404('Arquivo não encontrado')

    perfil = getattr(request.user, 'perfil', None)
    if not perfil:
        return HttpResponseForbidden('Acesso negado')

    if perfil.tipo == 'ADMIN':
        return FileResponse(open(arquivo_path, 'rb'))

    tenant = getattr(request, 'tenant', None)
    if not tenant:
        return HttpResponseForbidden('Acesso negado')

    return FileResponse(open(arquivo_path, 'rb'))
