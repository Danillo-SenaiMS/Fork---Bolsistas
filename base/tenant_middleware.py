from .tenant import set_current_tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = None
        if request.user.is_authenticated:
            perfil = getattr(request.user, 'perfil', None)
            if perfil and perfil.tenant_id:
                tenant = perfil.tenant
                set_current_tenant(tenant)
        request.tenant = tenant
        return self.get_response(request)
