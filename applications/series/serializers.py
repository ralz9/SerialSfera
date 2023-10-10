from rest_framework import serializers
from .models import Category, Serial, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SerialSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Serial
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['like_count'] = instance.likes.filter(is_like=True).count()


        return rep



class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Like
        fields = '__all__'
