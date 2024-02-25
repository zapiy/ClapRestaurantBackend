from rest_framework.serializers import ModelSerializer, CharField, ChoiceField
from mobile.models import MobileQuizQuestionModel
from .answer import QuizAnswerSerializer
from ..fields import AvatarField


class QuizQuestionSerializer(ModelSerializer):
    image = AvatarField(
        default_path="/static/media_defaults/quiz.jpg",
        path_format="/cdn/image/{0}.jpg",
        source="image_id"
    )
    type = ChoiceField(MobileQuizQuestionModel.Type.values)
    name = CharField(min_length=2, max_length=100)
    description = CharField(required=False, min_length=2, max_length=1000)
    answers = QuizAnswerSerializer(many=True)
    
    class Meta:
        model = MobileQuizQuestionModel
        fields = [
            'uuid', 'type', 'name', 'image', 'description', 
            'answers', 'created_at'
        ]
        read_only_fields = ['uuid', 'image', 'answers', 'created_at']


class FullQuizQuestionSerializer(QuizQuestionSerializer):
    correct_answer = QuizAnswerSerializer(many=True)
    
    class Meta(QuizQuestionSerializer.Meta):
        fields = [
            *QuizQuestionSerializer.Meta.fields,
            'correct_answer'
        ]
        read_only_fields = [
            *QuizQuestionSerializer.Meta.read_only_fields,
            'correct_answer'
        ]
