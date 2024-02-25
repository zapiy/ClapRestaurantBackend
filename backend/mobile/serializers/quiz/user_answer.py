from rest_framework.serializers import ModelSerializer
from mobile.models import MobileQuizUserAnswerModel
from .answer import QuizAnswerSerializer


class QuizUserAnswerSerializer(ModelSerializer):
    option_answer = QuizAnswerSerializer()
    
    class Meta:
        model = MobileQuizUserAnswerModel
        fields = [
            'uuid', 'status', 'text_answer', 
            'option_answer', 'created_at'
        ]
