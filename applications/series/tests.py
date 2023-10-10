from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from applications.account.models import CustomUser
from applications.series.models import Category, Serial
from applications.series.views import CategoryModelViewSet, SerialModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Create your tests here.

class CategoryTest(APITestCase):
    """
    Теты на модель категории
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user('test@test.com', '1', is_active=True)

    def test_get_category(self):
        request = self.factory.get('api/v1/product/category')
        view = CategoryModelViewSet.as_view({'get': 'list'})
        response = view(request)
        print(response)
        assert response.status_code == 200
        assert len(response.data) == 0


    def test_post_category(self):
        data = {
            'name': 'Test'
        }
        request = self.factory.post('api/v1/product/category', data)
        force_authenticate(request, self.user)
        view = CategoryModelViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == 201
        assert Category.objects.count() == 13
