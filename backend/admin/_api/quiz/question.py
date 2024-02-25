from django.core.exceptions import ValidationError
from django.http import HttpRequest
import orjson

from mobile.models import MobileQuizModel, MobileQuizQuestionModel, MobileQuizAnswerModel
from utils import SN, SNF
from utils.web import CustomJsonResponse
from cdn.utils import process_file, FileType, ensure_recycle
from .const import ensure_check_sprints


async def quiz_question(request: HttpRequest, uuid: str):
    if uuid == 'new':
        if request.method != 'POST':
            return CustomJsonResponse(status=404)
        model = MobileQuizQuestionModel()
    else:
        try:
            model = await MobileQuizQuestionModel.objects.aget(uuid = uuid)
        except (ValidationError, MobileQuizQuestionModel.DoesNotExist):
            return CustomJsonResponse(status=404)
    
    if request.method == "DELETE" and uuid != 'new':
        if "uuid" in request.POST:
            if request.POST["uuid"] == str(model.uuid):
                await ensure_recycle(model.image)
                await model.adelete()
                await ensure_check_sprints()
                return CustomJsonResponse(status=200)
            return CustomJsonResponse(status=406)
            
    elif request.method == "POST" and uuid == 'new':
        data = SN("_public").parse(request.POST, model)
        
        if data:
            quiz = SN.safe_get(request.POST, "quiz", SNF(str, null=False, validate=lambda v: len(v) in range(34, 40)))
            if not quiz:
                return CustomJsonResponse(status=406)
            
            try:
                data.quiz = await MobileQuizModel.objects.aget(uuid = quiz)
            except (ValidationError, MobileQuizModel.DoesNotExist):
                return CustomJsonResponse(status=406)
            
            if data.type == MobileQuizQuestionModel.Type.OPTION:  
                if (
                    "answers" not in request.POST
                    or "correct_answer" not in request.POST
                ):
                    return CustomJsonResponse(status = 406)

                try:
                    answers = [str(l).strip().title() for l in orjson.loads(request.POST['answers'])]
                    correct_answer = str(request.POST['correct_answer']).strip().title()
                    if correct_answer not in answers:
                        raise ValueError()
                except:
                    return CustomJsonResponse(status=406)

                if uuid == 'new':
                    await data.asave(force_insert=True)
                    for ans in answers:
                        ans_model = await MobileQuizAnswerModel.objects.acreate(
                            name = ans,
                            question = model
                        )
                        if ans == correct_answer:
                            model.correct_answer = ans_model
                else:
                    for ans in answers:
                        ans_model = (await MobileQuizAnswerModel.objects.aget_or_create(
                            name = ans,
                            defaults={
                                'question': model
                            }
                        ))[0]
                        if ans == correct_answer:
                            model.correct_answer = ans_model
                    
                    for ans in model.answers.all():
                        if ans.name not in answers:
                            await model.answers.aremove(ans)
            
            if "image" in request.FILES:
                await ensure_recycle(data.image)
                data.image = await process_file(request.FILES['image'], FileType.IMAGE)
            
            await data.asave(force_update=True)
        else:
            return CustomJsonResponse(status = 406)
    
    return CustomJsonResponse(SN("$public", "correct_answer").serialize(model))
