from django.urls import path

from . import views

urlpatterns = [
    path('', views.PainelBolsistasListView.as_view(), name='painel_lista'),
    path('<int:pk>/', views.PainelBolsistaDetailView.as_view(), name='painel_detalhe'),
    path('download/', views.painel_download_csv, name='painel_download_csv'),
]
