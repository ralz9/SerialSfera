import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from applications.series.tasks import send_notification_to_user

User = get_user_model()



class Category(models.Model):

    name = models.SlugField(primary_key=True, unique=True, max_length=50)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name


class Serial(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='serial')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='serial')
    title = models.CharField(max_length=89)
    video = models.FileField(upload_to='video')
    description = models.TextField('Описание')
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    series = models.CharField(max_length=100)
    vendor_code = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return f'{self.title}'



@receiver(pre_save, sender=Serial)
def generate_vendorcode(sender, instance, **kwargs):
    if not instance.vendor_code:
        # Генерируем случайное целое число от 1 до 1000
        instance.vendor_code = random.randint(1, 100000)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watched_serials = models.ManyToManyField(Serial, related_name='watched_by')
    bookmarks = models.ManyToManyField(Serial, related_name='bookmarked_by')



@receiver(post_save, sender=Serial)
def send_notification_on_new_series(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = CategorySubscription.objects.filter(category=category)
        for subscriber in subscribers:
            user = subscriber.owner
            send_notification_to_user.delay(user.email, instance.title, instance.series)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'serial')

    def __str__(self):
        return f'{self.user} -> {self.serial.title}'


class Like(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='likes'
    )
    serial = models.ForeignKey(
        Serial, on_delete=models.CASCADE,
        related_name='likes'
    )
    is_like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавляем поле created_at

    def __str__(self):
        return f'{self.owner} liked - {self.serial.title}'


class Rating(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings')
    serial = models.ForeignKey(
        Serial, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавляем поле created_at

    def __str__(self):
        return f'{self.owner} --> {self.serial.title}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    publications = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} -> {self.publications.title}'


class CategorySubscription(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscribed_by')

    class Meta:
        unique_together = ('owner', 'category')  # Ограничение на уникальность

    def __str__(self):
        return f"{self.owner} подписан на категорию {self.category.owner}"


