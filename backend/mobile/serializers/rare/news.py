from rest_framework.serializers import ModelSerializer, CharField
from mobile.models import MobileNewsModel
from ..fields import AvatarField, RichTextField


class NewsSerializer(ModelSerializer):
    image = AvatarField(
        default_path="/static/media_defaults/food.jpg",
        path_format="/cdn/image/{0}.jpg",
        source="image_id"
    )
    name = CharField(min_length=2, max_length=100)
    content = RichTextField(required=False)
    
    class Meta:
        model = MobileNewsModel
        fields = ['uuid', 'image', 'name', 'content', 'created_at']
        read_only_fields = ['uuid', 'image', 'created_at']
