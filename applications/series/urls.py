from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings
from .views import CategoryModelViewSet, SerialModelViewSet, CommentModelViewSet


router = DefaultRouter()
router.register('category', CategoryModelViewSet)
router.register('comments', CommentModelViewSet)
router.register('', SerialModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/series/recommendations/', SerialModelViewSet.as_view({'get': 'recommendations'}), name='serial-recommendations'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
