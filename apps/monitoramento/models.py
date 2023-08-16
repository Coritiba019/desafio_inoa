from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Ativo(models.Model):
    OPCOES_SETOR = [
        ("CONSUMER_CYCLICAL", "Consumo Cíclico"),
        ("CONSUMER_DEFENSIVE", "Consumo não Cíclico"),
        ("UTILITIES", "Utilidade Pública"),
        ("INDUSTRIALS", "Bens Industriais"),
        ("BASIC_MATERIALS", "Materiais Básicos"),
        ("FINANCIAL_SERVICES", "Financeiro e Outros"),
        ("TECHNOLOGY", "Tecnologia da Informação"),
        ("HEALTHCARE", "Saúde"),
        ("ENERGY", "Petróleo, Gás e Biocombustíveis"),
        ("COMMUNICATION_SERVICES", "Comunicações"),
        ("REAL_ESTATE", "Imóveis")
    ]

    codigo = models.CharField(max_length=10, unique=True, help_text="Código do Ativo, e.g., WEGE3")
    nome = models.CharField(max_length=100, help_text="Nome completo do Ativo")
    preco_atual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    variacao_preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    setor = models.CharField(max_length=100, choices=OPCOES_SETOR, default='', help_text="setor ao qual o ativo pertence")
    descricao = models.TextField(blank=True, null=True, help_text="Descrição adicional ou detalhes sobre o ativo")
    limite_inferior = models.DecimalField(max_digits=10, decimal_places=2, help_text="", null=True, blank=True)
    limite_superior = models.DecimalField(max_digits=10, decimal_places=2, help_text="", null=True, blank=True)
    periodicidade_checagem = models.PositiveIntegerField(help_text="Periodicidade da checagem em minutos", null=True, blank=True)
    ultima_atualizacao = models.DateTimeField(null=True, blank=True, help_text="Data e hora da última atualização do preço", default=timezone.now)
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="user"
    )


    def __str__(self):
        return f"{self.codigo} - {self.nome}"
