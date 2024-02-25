from django.http import HttpRequest
from django.core.exceptions import ValidationError

from mobile.models import MobileQuizModel, MobileQuizQuestionModel
from utils import SN
from utils.web import CustomJsonResponse, paginate


async def quizzes(request: HttpRequest):
    return paginate(
        request = request,
        data = MobileQuizModel.objects.order_by('-created_at').all(),
        serializer = SN("$public").serialize
    )

async def quiz_questions(request: HttpRequest, uuid: str):
    try:
        model = await MobileQuizModel.objects.aget(uuid = uuid)
    except (ValidationError, MobileQuizModel.DoesNotExist):
        return CustomJsonResponse({}, status=404)
    
    return paginate(
        request = request,
        data = MobileQuizQuestionModel.objects.filter(quiz = model).all(),
        serializer = SN("$public", correct_answer = SN("$public")).serialize
    )
