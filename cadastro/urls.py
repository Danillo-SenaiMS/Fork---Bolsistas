from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.CadastroCreateView.as_view(), name='cadastro_create'),
    path('', views.CadastroDetailView.as_view(), name='cadastro_detail'),
    path('<int:pk>/', views.CadastroDetailView.as_view(), name='cadastro_detail_pk'),
    path('<int:pk>/editar/', views.CadastroUpdateView.as_view(), name='cadastro_update_pk'),
    path('<int:pk>/curso/add/', views.curso_add, name='curso_add'),
    path('<int:pk>/curso/<int:curso_pk>/remove/', views.curso_remove, name='curso_remove'),
    path('<int:pk>/pos/add/', views.pos_add, name='pos_add'),
    path('<int:pk>/pos/<int:pos_pk>/remove/', views.pos_remove, name='pos_remove'),
    path('lista/', views.CadastroListView.as_view(), name='cadastro_list'),
    path('solicitar/', views.SolicitacaoMultiplaView.as_view(), name='solicitacao_criar'),
    path('solicitacoes/', views.SolicitacaoListView.as_view(), name='solicitacao_list'),
    path('solicitacoes/<int:pk>/revisar/', views.SolicitacaoRevisarView.as_view(), name='solicitacao_revisar'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]