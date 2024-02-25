from django.core.exceptions import ValidationError
from django.http import HttpRequest

from mobile.models import MobileQuizUserAnswerModel
from middleware import allowed_methods
from utils.web import CustomJsonResponse
from utils import SN, SNF
from mobile.api.views.quiz.const import ensure_check_sprint


@allowed_methods("POST")
async def sprint_answer_verify(request: HttpRequest, uuid: str):
    try:
        model = await MobileQuizUserAnswerModel.objects.aget(
            uuid = uuid,
            status = MobileQuizUserAnswerModel.Status.ON_VERIFICATION
        )
    except (ValidationError, MobileQuizUserAnswerModel.DoesNotExist):
        return CustomJsonResponse(status=404)
    
    valid = SN.safe_get(request.POST, "valid", SNF(bool))
    if valid is None:
        return CustomJsonResponse(status=403)

    model.status = (
        MobileQuizUserAnswerModel.Status.CORRECT
        if valid else
        MobileQuizUserAnswerModel.Status.INCORRENT
    )
    await model.asave(force_update=True)
    
    await ensure_check_sprint(model.sprint)

    return CustomJsonResponse(status=200)
    