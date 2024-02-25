from rest_framework.serializers import ModelSerializer, CharField
from mobile.models import MobileFoodCategoryModel
from ..fields import AvatarField


class PreviewFoodCategorySerializer(ModelSerializer):
    image = AvatarField(
        default_path="/static/media_defaults/food.jpg",
        path_format="/cdn/image/{0}.jpg",
        source="image_id"
    )
    name = CharField(min_length=2, max_length=100)
    class Meta:
        model = MobileFoodCategoryModel
        fields = ['uuid', 'image', 'name']
        read_only_fields = ['uuid', 'image']


class FoodCategorySerializer(PreviewFoodCategorySerializer):
    class Meta:
        model = MobileFoodCategoryModel
        fields = [
            *PreviewFoodCategorySerializer.Meta.fields, 
            'children'
        ]
        read_only_fields = [
            *PreviewFoodCategorySerializer.Meta.read_only_fields, 
            'children'
        ]
