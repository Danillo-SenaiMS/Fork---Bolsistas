from django.urls import path

from . import views

urlpatterns = [
    path('', views.PainelBolsistasListView.as_view(), name='painel_lista'),
    path('<int:pk>/', views.PainelBolsistaDetailView.as_view(), name='painel_detalhe'),
    path('<int:pk>/resumo/', views.gerar_resumo_view, name='painel_resumo_ia'),
    path('<int:pk>/analisar/', views.analisar_candidato_view, name='painel_analise_ia'),
    path('download/', views.painel_download_csv, name='painel_download_csv'),
]
