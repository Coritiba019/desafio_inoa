python manage.py runserver

celery -A setup beat -l INFO

celery -A setup worker -l INFO --pool=solo