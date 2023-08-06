from django.urls import path
from monitoramento.views import index, detalhes_ativo

urlpatterns = [
    path('', index, name='index'),
    path('ativo/', detalhes_ativo, name='detalhes_ativo')
]