from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from applications.series.models import Category, Serial, Like, Rating
from applications.series.serializers import CategorySerializer, SerialSerializer, RatingSerializer


# Create your views here.


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SerialModelViewSet(viewsets.ModelViewSet):
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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