from accounts.models import Perfil


def perfil_context(request):
    if not request.user.is_authenticated:
        return {
            'tipo_usuario': None,
            'has_cadastro': False,
        }
    if request.user.is_superuser:
        tipo = 'MANAGER'
    else:
        perfil = getattr(request.user, 'perfil', None)
        tipo = perfil.tipo if perfil else 'COMMON'
    return {
        'tipo_usuario': tipo,
        'has_cadastro': hasattr(request.user, 'cadastro'),
    }
