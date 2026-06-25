from django.http import FileResponse, Http404, HttpResponseForbidden
from django.conf import settings
from pathlib import Path

from accounts.models import DocumentoExterno
from .mixins import GROUP_MANAGER


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
        doc = DocumentoExterno.objects.filter(arquivo=path).first()
        if doc and doc.user == request.user:
            return FileResponse(open(arquivo_path, 'rb'))
        return HttpResponseForbidden('Acesso negado')

    return FileResponse(open(arquivo_path, 'rb'))
