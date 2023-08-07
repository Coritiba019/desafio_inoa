from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.monitoramento.urls')),
    path('', include('apps.usuarios.urls')),
]
