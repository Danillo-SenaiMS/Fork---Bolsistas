from django.urls import path
from . import views

urlpatterns = [
    path('criterios/', views.CriterioListView.as_view(), name='criterio_list'),
    path('criterios/criar/', views.CriterioCreateView.as_view(), name='criterio_create'),
    path('criterios/<int:pk>/editar/', views.CriterioUpdateView.as_view(), name='criterio_update'),
    path('', views.ClassificacaoListView.as_view(), name='classificacao_list'),
    path('criar/', views.ClassificacaoCreateView.as_view(), name='classificacao_create'),
    path('<int:pk>/', views.ClassificacaoDetailView.as_view(), name='classificacao_detail'),
    path('importar-csv/', views.CsvImportView.as_view(), name='csv_import'),
]
