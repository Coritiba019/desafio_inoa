from django import forms
from apps.monitoramento.models import Ativo

class AtivoForms(forms.ModelForm):
    class Meta:
        model = Ativo
        exclude = ('nome', 'preco_atual', 'caminho_imagem', 'descricao', 'setor', 'ultima_atualizacao', 'usuario', 'variacao_preco')

        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'limite_inferior': forms.TextInput(attrs={'class': 'form-control'}),
            'limite_superior': forms.TextInput(attrs={'class': 'form-control'}),
            'periodicidade_checagem': forms.TextInput(attrs={'class': 'form-control'}),
        }

