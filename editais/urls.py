from django.urls import path
from . import views

urlpatterns = [
    path('', views.EditalProvisorioListView.as_view(), name='edital_list'),
    path('resumo/', views.EditalListaResumoView.as_view(), name='edital_lista_resumo'),
    path('resumo/csv/', views.EditalListaResumoCSVView.as_view(), name='edital_lista_resumo_csv'),
    path('criar/', views.EditalProvisorioCreateView.as_view(), name='edital_create'),
    path('<int:pk>/', views.EditalProvisorioDetailView.as_view(), name='edital_detail'),
    path('<int:pk>/resumo/', views.EditalResumoView.as_view(), name='edital_resumo'),
    path('<int:pk>/pdf/', views.edital_pdf_view, name='edital_pdf'),
    path('<int:pk>/editar/', views.EditalProvisorioUpdateView.as_view(), name='edital_update'),
    path('<int:pk>/excluir/', views.EditalProvisorioDeleteView.as_view(), name='edital_delete'),
    path('<int:pk>/avaliar/', views.AvaliacaoCandidatosView.as_view(), name='avaliacao_candidatos'),
    path('<int:edital_pk>/avaliar/<int:aplicacao_pk>/', views.AvaliarCandidatoView.as_view(), name='avaliar_candidato'),
    path('<int:pk>/aplicar/', views.AplicarEditalView.as_view(), name='aplicar_edital'),
    path('aplicacoes/', views.AplicacaoListView.as_view(), name='aplicacao_list'),
    path('aplicacoes/<int:pk>/cancelar/', views.CancelarAplicacaoView.as_view(), name='cancelar_aplicacao'),
    path('aplicacoes/<int:pk>/nota/', views.SalvarNotaAplicacaoView.as_view(), name='salvar_nota_aplicacao'),
    path('aplicacoes/<int:pk>/status/', views.AlterarStatusAplicacaoView.as_view(), name='alterar_status_aplicacao'),
]
