from rest_framework.serializers import ModelSerializer, CharField, EmailField, DateField
from mobile.models import MobileNewsModel
from ..fields import AvatarField


class PreviewUserSerializer(ModelSerializer):
    avatar = AvatarField(
        default_path="/static/media_defaults/avatar.jpg",
        path_format="/cdn/image/{0}.jpg",
        source="avatar_id"
    )
    full_name = CharField(min_length=2, max_length=100)
    
    class Meta:
        model = MobileNewsModel
        fields = ['uuid', 'avatar', 'full_name']
        read_only_fields = ['uuid', 'avatar']


class UserSerializer(PreviewUserSerializer):
    email = EmailField()
    description = CharField(required=False, min_length=10, max_length=1000)
    birthday = DateField()
    working_at = DateField(required=False)
    
    class Meta(PreviewUserSerializer.Meta):
        fields = [
            *PreviewUserSerializer.Meta.fields,
            'email', 'description', 'status', 
            'birthday', 'working_at', 'updated_at', 'created_at'
        ]
        read_only_fields = [
            *PreviewUserSerializer.Meta.read_only_fields,
            'status', 'updated_at', 'created_at'
        ]
