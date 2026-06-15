from django.http import FileResponse, Http404, HttpResponseForbidden
from django.conf import settings
from pathlib import Path

from accounts.models import DocumentoExterno


def media_protegida(request, path):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Acesso negado')

    media_root = Path(settings.MEDIA_ROOT).resolve()
    arquivo_path = (media_root / path).resolve()

    if not str(arquivo_path).startswith(str(media_root)):
        return HttpResponseForbidden('Acesso negado')

    if not arquivo_path.exists() or not arquivo_path.is_file():
        raise Http404('Arquivo não encontrado')

    perfil = getattr(request.user, 'perfil', None)
    if not perfil:
        return HttpResponseForbidden('Acesso negado')

    if perfil.tipo == 'ADMIN':
        return FileResponse(open(arquivo_path, 'rb'))

    relative = path.replace('\\', '/')
    if relative.startswith('documentos/'):
        doc = DocumentoExterno.objects.filter(arquivo=path).first()
        if doc and doc.user == request.user and doc.tenant == getattr(request, 'tenant', None):
            return FileResponse(open(arquivo_path, 'rb'))
        return HttpResponseForbidden('Acesso negado')

    tenant = getattr(request, 'tenant', None)
    if not tenant:
        return HttpResponseForbidden('Acesso negado')

    return FileResponse(open(arquivo_path, 'rb'))
