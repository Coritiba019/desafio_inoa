from django.urls import path
from apps.monitoramento.views import index, detalhes_ativo, novo_ativo, editar_ativo, deletar_ativo, get_ativo_info, test, get_updated_ativos, get_data

urlpatterns = [
    path('', index, name='index'),
    path('ativo/<int:ativo_id>', detalhes_ativo, name='detalhes_ativo'),
    path('novo_ativo', novo_ativo, name='novo_ativo'),
    path('editar_ativo/<int:ativo_id>/', editar_ativo, name='editar_ativo'),
    path('deletar_ativo/<int:ativo_id>', deletar_ativo, name='deletar_ativo'),
    path('get_ativo_info/<int:ativo_id>/', get_ativo_info, name='get_ativo_info'),
    path('test', test, name='test'),
    path('api/updated_ativos/', get_updated_ativos, name='get_updated_ativos'),
    path('api/data/<str:codigo>/<str:range>/', get_data, name='get_data'),
]