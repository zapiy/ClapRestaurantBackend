from django.http import HttpRequest
from django.core.exceptions import ValidationError

from middleware import allowed_methods
from mobile.models import (
    MobileUserModel, MobileQuizQuestionModel, 
    MobileQuizUserAnswerModel, MobileQuizUserSprintModel,
    MobileQuizAnswerModel
)
from utils.web import CustomJsonResponse
from utils import SN, SNF
from .const import get_current_sprint, ensure_check_sprint


@allowed_methods("POST")
async def solve_quiz(request: HttpRequest, uuid: str):
    try:
        model = await MobileQuizQuestionModel.objects.aget(uuid = uuid)
    except (ValidationError, MobileQuizQuestionModel.DoesNotExist):
        return CustomJsonResponse(status=404)
    
    user: MobileUserModel = request._user
    
    sprint = await get_current_sprint(user, model.quiz)
    if sprint.status != MobileQuizUserSprintModel.Status.WHILE_TAKING:
        return CustomJsonResponse(status=406)
    
    answer = SN.safe_get(request.POST, "answer", SNF(str, validate=lambda v: len(v) in range(1, 1000)))
    if (
        answer is None
        or (
            await MobileQuizUserAnswerModel.objects.filter(
                sprint = sprint,
                question = model
            ).aexists()
        )
    ):
        return CustomJsonResponse(status=406)
    
    if model.type == model.Type.TEXT:
        await MobileQuizUserAnswerModel.objects.acreate(
            sprint = sprint,
            question = model,
            status = MobileQuizUserAnswerModel.Status.ON_VERIFICATION,
            text_answer = answer
        )
    
    elif model.type == model.Type.OPTION:
        try:
            answer_model = await MobileQuizAnswerModel.objects.filter(
                uuid = answer,
                question = model
            ).aget()
        except:
            return CustomJsonResponse(status=406)
        
        await MobileQuizUserAnswerModel.objects.acreate(
            sprint = sprint,
            question = model,
            option_answer = answer_model,
            status = (
                MobileQuizUserAnswerModel.Status.CORRECT
                if str(model.correct_answer_id) == answer else
                MobileQuizUserAnswerModel.Status.INCORRENT
            ),
        )
    
    return CustomJsonResponse({
        "can_next": await ensure_check_sprint(sprint),
    })
