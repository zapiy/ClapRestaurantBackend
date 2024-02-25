from rest_framework.serializers import ModelSerializer, CharField, BooleanField, IntegerField
from mobile.models import MobileQuizModel
from ..fields import AvatarField, RichTextField


class PreviewQuizSerializer(ModelSerializer):
    image = AvatarField(
        default_path="/static/media_defaults/quiz.jpg",
        path_format="/cdn/image/{0}.jpg",
        source="image_id"
    )
    name = CharField(min_length=2, max_length=100)
    
    class Meta:
        model = MobileQuizModel
        fields = ['uuid', 'image', 'name', 'created_at']
        read_only_fields = ['uuid', 'image', 'created_at']


class QuizSerializer(PreviewQuizSerializer):
    newbie_required = BooleanField(default=False)
    passing_percentage = IntegerField(min_value=1, max_value=100)
    content = RichTextField()
    
    class Meta:
        model = MobileQuizModel
        fields = [
            *PreviewQuizSerializer.Meta.fields, 
            'newbie_required', 'passing_percentage', 'content'
        ]


