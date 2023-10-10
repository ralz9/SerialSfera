from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from django.conf import settings
from .views import CategoryModelViewSet, SerialModelViewSet

router = DefaultRouter()
router.register('category', CategoryModelViewSet)
router.register('', SerialModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
