from django.contrib import admin
from .models import (
    CadastroBolsista, FormacaoAcademica, ExperienciaProfissional,
    AnexoComprobatorio, SolicitacaoEdicao,
)


@admin.register(CadastroBolsista)
class CadastroBolsistaAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefone', 'cidade', 'estado', 'pontuacao_previa', 'tenant', 'created_at']
    list_filter = ['tenant', 'estado']
    search_fields = ['user__email', 'user__nome_completo', 'cidade', 'rua']


@admin.register(FormacaoAcademica)
class FormacaoAcademicaAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'tipo', 'status', 'area', 'curso', 'ano_conclusao']
    list_filter = ['tipo', 'status']
    search_fields = ['bolsista__user__nome_completo', 'curso', 'area']


@admin.register(ExperienciaProfissional)
class ExperienciaProfissionalAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'area_atuacao', 'anos_experiencia', 'anexo', 'created_at']
    list_filter = ['tenant']
    search_fields = ['bolsista__user__nome_completo', 'area_atuacao']


@admin.register(AnexoComprobatorio)
class AnexoComprobatorioAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'tipo', 'anexo', 'created_at']
    list_filter = ['tipo', 'tenant']
    search_fields = ['bolsista__user__nome_completo', 'tipo']


@admin.register(SolicitacaoEdicao)
class SolicitacaoEdicaoAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'campo', 'valor_original', 'valor_novo', 'status', 'created_at']
    list_filter = ['status', 'campo']
    search_fields = ['bolsista__user__nome_completo', 'campo']
