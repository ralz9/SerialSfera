from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryModelViewSet, SerialModelViewSet

router = DefaultRouter()
router.register('category', CategoryModelViewSet)
router.register('', SerialModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
