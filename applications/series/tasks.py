from django.core.mail import send_mail
from config.celery import app
from django.shortcuts import redirect

@app.task
def send_notification_to_user(email, serial_title, series_title):
    send_mail(
        'New Series Available',
        f'Hello, a new series "{series_title}" is now available for the serial "{serial_title}". Check it out!',
        'RodionDereha@gmail.com',
        [email]
    )

