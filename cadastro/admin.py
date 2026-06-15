from django.contrib import admin
from .models import CadastroBolsista, CursoSuperior, PosGraduacao, SolicitacaoEdicao


@admin.register(CadastroBolsista)
class CadastroBolsistaAdmin(admin.ModelAdmin):
    list_display = ['user', 'grau_academico', 'tenant', 'created_at']
    list_filter = ['grau_academico']


@admin.register(CursoSuperior)
class CursoSuperiorAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'curso', 'instituicao', 'grau']


@admin.register(PosGraduacao)
class PosGraduacaoAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'tipo', 'area', 'instituicao']


@admin.register(SolicitacaoEdicao)
class SolicitacaoEdicaoAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'campo', 'status', 'created_at']
    list_filter = ['status']
