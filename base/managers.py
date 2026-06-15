from django.db import models
from .tenant import get_current_tenant


class TenantManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        tenant = get_current_tenant()
        if tenant is not None:
            return qs.filter(tenant=tenant)
        return qs

    def all_for_tenant(self, tenant=None):
        if tenant is None:
            tenant = get_current_tenant()
        if tenant is not None:
            return super().get_queryset().filter(tenant=tenant)
        return super().get_queryset()
