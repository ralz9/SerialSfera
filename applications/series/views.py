from django.db.models import Min, Max, Count
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from applications.series.models import Category, Serial, Like, Rating, Comment, Favorite
from applications.series.serializers import CategorySerializer, SerialSerializer, RatingSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SerialModelViewSet(viewsets.ModelViewSet):
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Добавляем DjangoFilterBackend
    filterset_fields = {
        'created_at': ['gte', 'lte'],  # Фильтр по дате создания
        'ratings__rating': ['gte', 'lte'],
    }
    search_fields = ['title']

    pagination_class = PageNumberPagination
    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        user = request.user

        if user.is_anonymous:
            return Response({'error': 'Только аутентифицированные пользователи могут добавлять сериалы в избранное'},
                            status=401)

        serial = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=user, serial=serial)

        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'})
        else:
            return Response({'status': 'added to favorites'})

    @action(detail=False, methods=['GET'])
    def favorites(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        favorite_serials = [favorite.serial for favorite in favorites]
        serialized_favorites = SerialSerializer(favorite_serials, many=True)
        return Response(serialized_favorites.data)

    @action(detail=False, methods=['GET'])
    def recommendations(self, request):
        recommended_serials = Serial.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:10]
        serialized_recommendations = SerialSerializer(recommended_serials, many=True)
        return Response(serialized_recommendations.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        min_rating = self.request.query_params.get('min_rating', None)
        max_rating = self.request.query_params.get('max_rating', None)

        if min_rating is not None:
            queryset = queryset.annotate(min_rating=Min('ratings__rating')).filter(min_rating__gte=min_rating)

        if max_rating is not None:
            queryset = queryset.annotate(max_rating=Max('ratings__rating')).filter(max_rating__lte=max_rating)

        queryset = queryset.annotate(total_likes=Count('likes__is_like')).order_by('-total_likes')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @authentication_classes([SessionAuthentication])
    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        user = request.user

        if user.is_anonymous:
            return Response({'error': 'Только аутентифицированные пользователи могут выполнять это действие'},
                            status=401)

        like_obj, _ = Like.objects.get_or_create(owner=user, serial_id=pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        like_status = 'liked'
        if not like_obj.is_like:
            like_status = 'unliked'

        return Response({'status': like_status})

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        user = request.user
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(owner=request.user, serial_id=pk)
        rating_obj.rating = serializer.data['rating']
        rating_obj.save()
        return Response(serializer.data)


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)