from django.core.mail import send_mail
from config.celery import app


@app.task
def send_activation_code(email, code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{code}'
    image_url = 'http://35.198.162.176/media/video/photo_2023-10-16_21-05-20_H4jacsr.jpg'
    message = f'Привет, нажми на "Активировать" чтобы активировать аккаунт:<br><a href="{activation_url}">Активировать</a><br>'
    message += f'<img src="{image_url}" alt="image">'
    send_mail(
        'Activation code',
        '',
        # f'Привет перейди по ссылке что бы активировать аккаунт http:/localhost:8000/api/v1/account/activate/{code}',
        'a.kudaikulov04@gmail.com',
        [email],
        html_message=message
    )


@app.task
def send_forgot_password_code(email, code):
    send_mail(
        'Extra theme py29',
        f'Вот ваш код для восстановления пароля, никому не показывайте его: {code}',
        'RodionDereha@gmail.com',
        [email]
    )

