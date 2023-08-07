# email_test.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

# Function for sending test email
def send_test_email():
    send_mail(
        subject='Teste de envio de email',
        message='Se você está lendo isso, o envio de email está funcionando!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['coritiba019@gmail.com'],
        fail_silently=True,
    )

send_test_email()