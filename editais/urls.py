from django.urls import path
from . import views

urlpatterns = [
    path('', views.EditalListView.as_view(), name='edital_list'),
    path('criar/', views.EditalCreateView.as_view(), name='edital_create'),
    path('<int:pk>/', views.EditalDetailView.as_view(), name='edital_detail'),
    path('<int:pk>/editar/', views.EditalUpdateView.as_view(), name='edital_update'),
    path('<int:pk>/aplicar/', views.AplicarEditalView.as_view(), name='aplicar_edital'),
    path('aplicacoes/', views.AplicacaoListView.as_view(), name='aplicacao_list'),
    path('aplicacoes/<int:pk>/cancelar/', views.CancelarAplicacaoView.as_view(), name='cancelar_aplicacao'),
    path('aplicacoes/<int:pk>/status/', views.AlterarStatusAplicacaoView.as_view(), name='alterar_status_aplicacao'),
]
