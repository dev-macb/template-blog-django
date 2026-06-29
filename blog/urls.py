from django.urls import path

from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('<slug:slug>/', views.detalhe_publicacao, name='detalhe_publicacao'),
]
