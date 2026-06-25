from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.CadastroCreateView.as_view(), name='cadastro_create'),
    path('', views.CadastroDetailView.as_view(), name='cadastro_detail'),
    path('<int:pk>/', views.CadastroDetailView.as_view(), name='cadastro_detail_pk'),
    path('<int:pk>/editar/', views.CadastroUpdateView.as_view(), name='cadastro_update_pk'),
    path('<int:pk>/formacao/add/', views.formacao_add, name='formacao_add'),
    path('<int:pk>/formacao/<int:formacao_pk>/remove/', views.formacao_remove, name='formacao_remove'),
    path('lista/', views.CadastroListView.as_view(), name='cadastro_list'),
    path('solicitar/', views.SolicitacaoMultiplaView.as_view(), name='solicitacao_criar'),
    path('solicitacoes/', views.SolicitacaoListView.as_view(), name='solicitacao_list'),
    path('solicitacoes/<int:pk>/revisar/', views.SolicitacaoRevisarView.as_view(), name='solicitacao_revisar'),
]
