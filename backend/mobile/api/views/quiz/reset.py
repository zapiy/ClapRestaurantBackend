from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.db.models.functions import Coalesce

from mobile.models import MobileQuizModel, MobileUserModel, MobileQuizUserSprintModel
from utils.web import CustomJsonResponse


async def reset_quiz_progress(request: HttpRequest, uuid: str):
    try:
        quiz = (
            await MobileQuizModel.objects
                .annotate(max_progress = Coalesce(Count('questions'), 0))
                .aget(uuid = uuid)
        )
        user: MobileUserModel = request._user
        sprint = await MobileQuizUserSprintModel.objects.aget(
            ~Q(status = MobileQuizUserSprintModel.Status.INCORRENT),
            user = user,
            quiz = quiz,
        )
    except (
        ValidationError, 
        MobileQuizModel.DoesNotExist,
        MobileQuizUserSprintModel.DoesNotExist,
    ):
        return CustomJsonResponse(status=404)

    await sprint.adelete()
    return CustomJsonResponse(status=200)
