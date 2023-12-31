# Generated by Django 4.2.4 on 2023-08-06 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(help_text='Código do Ativo, e.g., WEGE3', max_length=10, unique=True)),
                ('nome', models.CharField(help_text='Nome completo do Ativo', max_length=100)),
                ('preco_atual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('caminho_imagem', models.CharField(blank=True, help_text='URL ou caminho da imagem do ativo', max_length=200, null=True)),
                ('descricao', models.TextField(blank=True, help_text='Descrição adicional ou detalhes sobre o ativo', null=True)),
                ('limite_inferior_tunnel', models.DecimalField(decimal_places=2, help_text='Limite inferior do túnel de preço', max_digits=10)),
                ('limite_superior_tunnel', models.DecimalField(decimal_places=2, help_text='Limite superior do túnel de preço', max_digits=10)),
                ('periodicidade_checagem', models.PositiveIntegerField(help_text='Periodicidade da checagem em minutos')),
                ('ultima_atualizacao', models.DateTimeField(blank=True, help_text='Data e hora da última atualização do preço', null=True)),
            ],
        ),
    ]
