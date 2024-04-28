
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pedido_compra/', include('Pedido.urls')),
    path('', include('Pedido.urls')),
    path('autenticacao/', include('Autenticacao.urls'))
]
