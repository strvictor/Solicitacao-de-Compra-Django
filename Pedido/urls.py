from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostra_form, name="mostra_form")
]