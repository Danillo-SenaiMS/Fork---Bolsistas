from django.contrib import admin

from .models import Notificacao


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'destinatario', 'tipo', 'lido', 'created_at']
    list_filter = ['tipo', 'lido', 'tenant']
    search_fields = ['titulo', 'mensagem', 'destinatario__email']

