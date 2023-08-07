from django.contrib import admin
from monitoramento.models import Ativo

class ListandoAtivos(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nome', 'preco_atual', 'setor', 'ultima_atualizacao',)
    list_display_links = ('id', 'codigo',)
    search_fields = ('codigo', 'nome',)
    list_filter = ('setor',)
    list_per_page = 10

admin.site.register(Ativo, ListandoAtivos)
