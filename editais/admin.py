from django.contrib import admin
from .models import Edital, AplicacaoEdital


@admin.register(Edital)
class EditalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'status', 'data_abertura', 'data_fechamento', 'tenant']
    list_filter = ['status']


@admin.register(AplicacaoEdital)
class AplicacaoEditalAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'edital', 'status', 'data_aplicacao']
    list_filter = ['status']
