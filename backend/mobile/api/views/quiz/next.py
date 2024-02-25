from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.db.models.functions import Coalesce

from mobile.models import MobileQuizModel, MobileQuizQuestionModel, MobileQuizUserSprintModel, MobileUserModel
from utils.web import CustomJsonResponse
from utils import SN
from .const import get_current_sprint


async def get_next_quiz(request: HttpRequest, uuid: str):
    try:
        model = (
            await MobileQuizModel.objects
                .annotate(
                    max_progress = Coalesce(Count('questions'), 0)
                )
                .aget(uuid = uuid)
        )
    except (ValidationError, MobileQuizModel.DoesNotExist):
        return CustomJsonResponse(status=404)

    user: MobileUserModel = request._user
    
    sprint = await get_current_sprint(user, model)
    
    if sprint.status != MobileQuizUserSprintModel.Status.WHILE_TAKING:
        return CustomJsonResponse({
            'next': None,
            'status': sprint.status,
            'progress': model.max_progress,
            'max': model.max_progress,
        })
    
    next = (
        await MobileQuizQuestionModel.objects
            .filter(
                ~Q(user_answers__sprint = sprint),
                quiz = model,
            )
            .order_by('?')
            .afirst()
    )
    
    
    return CustomJsonResponse({
        'next': SN("$public").serialize(next),
        'status': MobileQuizUserSprintModel.Status.WHILE_TAKING,
        'progress': await sprint.answers.acount(),
        'max': model.max_progress,
    })
