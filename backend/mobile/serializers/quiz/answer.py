from rest_framework.serializers import ModelSerializer, CharField
from mobile.models import MobileQuizAnswerModel


class QuizAnswerSerializer(ModelSerializer):
    name = CharField(min_length=2, max_length=100)
    
    class Meta:
        model = MobileQuizAnswerModel
        fields = ['uuid', 'name']
