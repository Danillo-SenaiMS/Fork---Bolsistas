from django.urls import path
from . import views

urlpatterns = [
    path('', views.EditalProvisorioListView.as_view(), name='edital_list'),
    path('criar/', views.EditalProvisorioCreateView.as_view(), name='edital_create'),
    path('<int:pk>/', views.EditalProvisorioDetailView.as_view(), name='edital_detail'),
    path('<int:pk>/pdf/', views.edital_pdf_view, name='edital_pdf'),
    path('<int:pk>/editar/', views.EditalProvisorioUpdateView.as_view(), name='edital_update'),
    path('<int:pk>/excluir/', views.EditalProvisorioDeleteView.as_view(), name='edital_delete'),
    path('<int:pk>/aplicar/', views.AplicarEditalView.as_view(), name='aplicar_edital'),
]
