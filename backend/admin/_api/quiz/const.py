from django.db.models import Count, Q

from mobile.app_messaging import AppMessaging
from mobile.api.views.quiz.const import ensure_check_sprint
from mobile.models import (
    MobileUserModel, MobileQuizModel,
    MobileQuizUserSprintModel, MobileQuizUserAnswerModel
)


async def ensure_check_newbie():
    query = (
        MobileUserModel.objects
            .annotate(
                current_progress = Count(
                    "quiz_sprints",
                    filter=Q(
                        quiz_sprints__status = MobileQuizUserSprintModel.Status.CORRECT,
                        quiz_sprints__quiz__newbie_required = True
                    )
                )
            )
            .filter(status = MobileUserModel.Status.NEWBIE)
    )
    if await query.aexists():
        required_count = (
            await MobileQuizModel.objects
                .filter(newbie_required = True)
                .acount()
        )
        async for user in query.filter(
            current_progress__gte = required_count
        ).all():
            user.status = MobileUserModel.Status.ACTIVE
            await user.asave(force_update=True)
            await AppMessaging.newbie_promotion(user)


async def ensure_check_sprints():
    query = (
        MobileQuizUserSprintModel.objects
            .annotate(
                pending_count = Count(
                    "answers",
                    filter=Q(
                        answers__status = MobileQuizUserAnswerModel.Status.ON_VERIFICATION,
                    )
                ),
            )
            .filter(
                status = MobileQuizUserSprintModel.Status.ON_VERIFICATION,
                pending_count = 0
            )
    )
    if await query.aexists():
        async for sprint in query.all():
            await ensure_check_sprint(sprint)
