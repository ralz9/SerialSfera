from django.contrib import admin
from .models import UserProfile
from .views import Category, Serial


admin.site.register(Category)
admin.site.register(Serial)
