from rest_framework.serializers import ModelSerializer
from mobile.models import MobileQuizUserSprintModel
from .quiz import PreviewQuizSerializer
from ..rare import PreviewUserSerializer


class QuizUserSprintSerializer(ModelSerializer):
    quit = PreviewQuizSerializer()
    user = PreviewUserSerializer()
    
    class Meta:
        model = MobileQuizUserSprintModel
        fields = ['uuid', 'quiz', 'user', 'status', 'finished_at', 'created_at']
