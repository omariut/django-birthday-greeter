
from celery.schedules import crontab

# Celery Beat schedule
CELERY_BROKER_URL = 'redis://redis:6394/0'  

CELERY_BEAT_SCHEDULE = {
    'send-birthday-wishes': {
        'task': 'customers.tasks.send_birthday_wishes',
        'schedule': crontab(hour=23, minute=55),  # Run every day at 11:55 PM
    },
}