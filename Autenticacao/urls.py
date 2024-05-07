from django.urls import path
from . import views

urlpatterns = [
    path('', views.autenticacao, name="autenticacao"),
    path('home/', views.home, name="home"),
    path('aprovar/', views.aprovar_dado, name='aprovar_dado'),
    path('reprovar/', views.reprovar_dado, name='reprovar_dado'),
]