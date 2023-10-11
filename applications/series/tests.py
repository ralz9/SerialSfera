from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

from applications.account.models import CustomUser
from applications.series.models import Category, Serial
from applications.series.views import CategoryModelViewSet, SerialModelViewSet


class CategoryTest(APITestCase):
    """
    Теты на модель категории
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user('test@test.com', '1', is_active=True)

    def test_get_category(self):
        request = self.factory.get('api/v1/series/category')
        view = CategoryModelViewSet.as_view({'get': 'list'})
        response = view(request)
        print(response)
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_post_category(self):
        data = {
            'name': 'Test'
        }
        request = self.factory.post('api/v1/series/category', data)
        force_authenticate(request, self.user)
        view = CategoryModelViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == 201
        assert Category.objects.count() == 1


class SeriesTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user('test@test.com', '1', is_active=True)
        self.set_up_category()
        self.access_token = self.set_up_token()

    def set_up_token(self):
        data = {
            'email': 'test@test.com',
            'password': '1'
        }
        request = self.factory.post('api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()
        response = view(request)
        return response.data.get('access')

    @staticmethod
    def set_up_category():
        Category.objects.create(name='test')

    def test_get_series(self):
        request = self.factory.get('api/v1/series/', HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        # force_authenticate(request, self.user)
        view = SerialModelViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_post_series(self):
        video = open('video/photo_2023-09-28_04-56-57.jpg', 'rb')
        data = {
            'owner': self.user.id,
            'category': Category.objects.first().name,
            'title': 'test series',
            'video': video,
            'description': 'dead',
        }
        request = self.factory.post('api/v1/series/', data=data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        video.close()
        view = SerialModelViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == 201
        assert response.data.get('title') == 'test series'
        assert Serial.objects.count() > 0
