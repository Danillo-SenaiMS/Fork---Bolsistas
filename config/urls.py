from django.contrib import admin
from django.urls import path, include

from base.views import media_protegida

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('cadastro/', include('cadastro.urls')),
    path('editais/', include('editais.urls')),
    path('notificacoes/', include('notifications.urls')),
    path('classificacao/', include('classificacao.urls')),
    path('painel/', include('painel_bolsistas.urls')),

    path('media/<path:path>', media_protegida, name='protected_media'),
]
