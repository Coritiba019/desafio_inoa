from celery import shared_task
from apps.monitoramento.models import Ativo
import yfinance as yf
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True)
def checar_cotacoes(self):
    agora = timezone.now()

    for ativo in Ativo.objects.all():
        if ativo.ultima_atualizacao + timedelta(minutes=ativo.periodicidade_checagem) <= agora:

            ticker_data = yf.Ticker(ativo.codigo + ".SA")

            try:
                preco_atual = ticker_data.history(period="1d")['Close'].iloc[0]
            except IndexError:
                continue

            ativo.preco_atual = preco_atual
            ativo.ultima_atualizacao = agora

            user_email = ativo.usuario.email  # Extracting the email of the user associated with the asset

            # Check if the price is outside the limits
            if preco_atual < ativo.limite_inferior:
                send_notification_email(
                    subject='Notificação de Compra',
                    message=f'O preço de {ativo.codigo} caiu abaixo do limite! Atual: {preco_atual}, Limite: {ativo.limite_inferior}. Considere comprar.',
                    email=user_email
                )
            elif preco_atual > ativo.limite_superior:
                send_notification_email(
                    subject='Notificação de Venda',
                    message=f'O preço de {ativo.codigo} subiu acima do limite! Atual: {preco_atual}, Limite: {ativo.limite_superior}. Considere vender.',
                    email=user_email
                )

            ativo.save()

    return 'Done'

def send_notification_email(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )
