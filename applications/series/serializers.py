from rest_framework import serializers
from .models import Category, Serial, Like, Rating, Comment, CategorySubscription


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'


class SerialSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Serial
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['like_count'] = instance.likes.filter(is_like=True).count()

        rating_result = 0
        for rating in instance.ratings.all():
            rating_result += rating.rating

        if rating_result:
            rep['rating'] = rating_result / instance.ratings.all().count()
        else:
            rep['rating'] = 0

        return rep


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Like
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('rating',)


# class CategorySubscriptionSerializer(serializers.Serializer):
#     name_category = serializers.CharField(max_length=50)

# class CategorySubscriptionSerializer(serializers.Serializer):
#     name_category = serializers.CharField(max_length=50)
#
#     def validate_name_category(self, data):
#         request = self.context.get('request')
#         user = request.user
#         name_category = data.get('name_category')
#
#         try:
#             category = Category.objects.get(category_id=name_category)
#         except Category.DoesNotExist:
#             raise serializers.ValidationError("Категория с таким именем не существует.")
#
#         return data

class CategorySubscriptionSerializer(serializers.Serializer):
    name_category = serializers.CharField(max_length=50)

class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = CategorySubscription
        fields = '__all__'

    def get_owner(self, obj):
        return obj.owner.email



