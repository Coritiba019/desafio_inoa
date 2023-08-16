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
                daily_data = ticker_data.history(period="2d")  # Pega os dados dos últimos 2 dias.
                current_close = daily_data['Close'].iloc[-1]
                
                # Se temos pelo menos 2 dias de dados, pegamos o fechamento do dia anterior.
                if len(daily_data) > 1:
                    previous_close = daily_data['Close'].iloc[-2]
                else:
                    previous_close = 0
                
            except IndexError:
                continue

            # Calculando a variação percentual com base no preço de fechamento anterior e no preço de fechamento atual.
            if previous_close != 0:
                ativo.variacao_preco = ((current_close - previous_close) / previous_close) * 100
            else:
                ativo.variacao_preco = 0

            ativo.preco_atual = current_close
            ativo.ultima_atualizacao = agora

            user_email = ativo.usuario.email  # Extraindo o e-mail do usuário associado ao ativo.

            # Verificando se o preço está fora dos limites.
            if current_close < ativo.limite_inferior:
                send_notification_email(
                    subject='Notificação de Compra',
                    message=f'O preço de {ativo.codigo} caiu abaixo do limite! Atual: {current_close:.2f}, Limite: {ativo.limite_inferior}. Considere comprar.',
                    email=user_email
                )
            elif current_close > ativo.limite_superior:
                send_notification_email(
                    subject='Notificação de Venda',
                    message=f'O preço de {ativo.codigo} subiu acima do limite! Atual: {current_close:.2f}, Limite: {ativo.limite_superior}. Considere vender.',
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
