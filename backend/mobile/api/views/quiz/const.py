import pendulum
from django.core.exceptions import ValidationError
from django.db.models import Q

from mobile.app_messaging import AppMessaging
from mobile.models import (
    MobileUserModel, MobileQuizModel, 
    MobileQuizUserSprintModel, MobileQuizUserAnswerModel
)


async def get_current_sprint(user: MobileUserModel, quiz: MobileQuizModel):
    try:
        return await MobileQuizUserSprintModel.objects.aget(
            ~Q(status = MobileQuizUserSprintModel.Status.INCORRENT),
            user = user,
            quiz = quiz,
        )
    except (ValidationError, MobileQuizUserSprintModel.DoesNotExist):
        return await MobileQuizUserSprintModel.objects.acreate(
            user = user,
            quiz = quiz,
        )
        

async def ensure_check_sprint(sprint: MobileQuizUserSprintModel):
    questions_count = await sprint.quiz.questions.acount()
    
    if sprint.status == MobileQuizUserSprintModel.Status.WHILE_TAKING:
        if (questions_count != (await sprint.answers.acount())):
            return True
        sprint.status = MobileQuizUserSprintModel.Status.ON_VERIFICATION
        sprint.finished_at = pendulum.now()
        await sprint.asave(force_update=True)
    
    elif sprint.status != MobileQuizUserSprintModel.Status.ON_VERIFICATION:
        return (sprint.status == MobileQuizUserSprintModel.Status.CORRECT)
    
    fail_count = (
        await sprint.answers
            .filter(status = MobileQuizUserAnswerModel.Status.INCORRENT)
            .acount()
    )
    if fail_count > 0:
        fail_percentage = int((fail_count / questions_count) * 100)
        min_percentage = 100 - sprint.quiz.passing_percentage
        if fail_percentage >= min_percentage:
            sprint.status = MobileQuizUserSprintModel.Status.INCORRENT
            await sprint.asave(force_update=True)
            return False
    
    if not (
        await sprint.answers
            .filter(status = MobileQuizUserAnswerModel.Status.ON_VERIFICATION)
            .aexists()
    ):
        sprint.status = MobileQuizUserSprintModel.Status.CORRECT
        await sprint.asave(force_update=True)
        
        if sprint.user.status == MobileUserModel.Status.NEWBIE:
            if (
                (await MobileQuizUserSprintModel.objects
                    .filter(
                        user = sprint.user,
                        status = MobileQuizUserSprintModel.Status.CORRECT,
                        quiz__newbie_required = True
                    )
                    .acount())
                >=
                (await MobileQuizModel.objects.filter(
                    newbie_required = True).acount())
            ):
                sprint.user.status = MobileUserModel.Status.ACTIVE
                await sprint.user.asave(force_update=True)
                await AppMessaging.newbie_promotion(sprint.user)
    
    return True
