import threading

_active = threading.local()


def get_current_tenant():
    return getattr(_active, 'tenant', None)


def set_current_tenant(tenant):
    _active.tenant = tenant
