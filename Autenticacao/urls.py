from django.urls import path
from . import views


urlpatterns = [
    path('', views.autenticacao, name="autenticacao"),
    path('pedidos-pendentes/', views.pedidos_pendentes, name="pedidos_pendentes"),
    path('aprovar/', views.aprovar_dado, name='aprovar_dado'),
    path('reprovar/', views.reprovar_dado, name='reprovar_dado'),
    path('pedidos-aprovados/', views.pedidos_aprovados, name='pedidos_aprovados'),
    path('pedidos-reprovados/', views.pedidos_reprovados, name='pedidos_reprovados'),
    path('enviar-email/', views.enviar_email, name='enviar_email'),

]