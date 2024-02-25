from rest_framework.serializers import ModelSerializer, CharField
from mobile.models import MobileFoodModel
from .category import PreviewFoodCategorySerializer
from ..fields import AvatarField, RichTextField


class FoodSerializer(ModelSerializer):
    image = AvatarField(
        default_path="/static/media_defaults/food.jpg",
        path_format="/cdn/image/{0}.jpg",
        source="image_id"
    )
    name = CharField(min_length=2, max_length=100)
    category = PreviewFoodCategorySerializer()
    content = RichTextField(required=False)
    
    class Meta:
        model = MobileFoodModel
        fields = ['uuid', 'image', 'name', 'category', 'content', 'created_at']
        read_only_fields = ['uuid', 'image', 'category', 'created_at']
