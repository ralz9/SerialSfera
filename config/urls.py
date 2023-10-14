from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="SerialSfera.kg",
      default_version='v1',
      description="Contacs is we"
                  "we for WhatsApp: +996 507812318 \n"
                  "we for instagram SerialSfera.kg \n"
                  "we for telegram SerialSfera.kg \n "
                  "we for facebook SerialSfera.kg \n ",
      contact=openapi.Contact(email="SerialSfera@2000.com"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('applications.account.urls')),
    path('api/v1/series/', include('applications.series.urls')),
    path('swagger/', schema_view.with_ui('swagger')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



