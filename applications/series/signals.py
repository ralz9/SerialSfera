from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Serial, CategorySubscription  # Замените 'yourapp' на фактическое имя вашего приложения
from .views import send_series_notification_to_subscribers  # Импортируйте функцию уведомления

@receiver(post_save, sender=Series)
def send_series_notification(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        send_series_notification_to_subscribers(category)
