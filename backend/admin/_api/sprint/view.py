from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.db.models import (
    Count, Q, Subquery, OuterRef,
    IntegerField, CharField, Value
)
from django.db.models.functions import Coalesce

from utils import SN
from utils.web import CustomJsonResponse, paginate
from mobile.models import (
    MobileUserModel, MobileQuizModel,
    MobileQuizUserAnswerModel, MobileQuizUserSprintModel
)

async def quizzes_sprints(request: HttpRequest):
    users_count = (
        await MobileUserModel.objects
            .filter(~Q(status = MobileUserModel.Status.LEAVE))
            .acount()
    )
    sprint_count_query = lambda status: (
        Coalesce(
            Subquery(
                MobileQuizUserSprintModel.objects
                    .filter(
                        status = status,
                        quiz = OuterRef('uuid'),
                    )
                    .values_list(Count('uuid'))[:1]
            ), 0,
            output_field=IntegerField()
        )
    )
    
    return paginate(
        request = request,
        side_data={
            "users_count": users_count,
        },
        data = (
            MobileQuizModel.objects
                .annotate(
                    passed_count = sprint_count_query(
                        MobileQuizUserSprintModel.Status.CORRECT),
                    pending_count = sprint_count_query(
                        MobileQuizUserSprintModel.Status.ON_VERIFICATION),
                    processing_count = sprint_count_query(
                        MobileQuizUserSprintModel.Status.WHILE_TAKING),
                )
                .order_by('-pending_count')
        ),
        serializer = SN(
            "$preview", "passed_count",
            "pending_count", "processing_count",
        ).serialize
    )
    

async def quiz_users_sprints(request: HttpRequest, uuid: str):
    try:
        quiz = await MobileQuizModel.objects.aget(uuid = uuid)
    except (ValidationError, MobileQuizModel.DoesNotExist):
        return CustomJsonResponse({}, status=404)
    
    return paginate(
        request = request,
        side_data= {
            "quiz": SN("$preview").serialize(quiz),
        },
        data = (
            MobileUserModel.objects
                .filter(~Q(status = MobileUserModel.Status.LEAVE))
                .annotate(
                    incorrect_attempts = Coalesce(
                        Subquery(
                            MobileQuizUserSprintModel.objects
                                .filter(
                                    status = MobileQuizUserSprintModel.Status.INCORRENT,
                                    quiz = quiz,
                                    user = OuterRef('uuid'),
                                )
                                .values_list(Count('uuid'))[:1]
                        ), 0,
                        output_field=IntegerField()
                    ),
                    current_status = Coalesce(
                        Subquery(
                            MobileQuizUserSprintModel.objects
                                .filter(
                                    ~Q(status = MobileQuizUserSprintModel.Status.INCORRENT),
                                    quiz = quiz,
                                    user = OuterRef('uuid'),
                                )
                                .values_list('status')
                        ), Value("not started"),
                        output_field=CharField()
                    ),
                    need_verify = Q(
                        current_status = MobileQuizUserSprintModel.Status.ON_VERIFICATION),
                )
                .order_by('-need_verify')
        ),
        serializer = SN(
            "$preview", "incorrect_attempts", "current_status",
        ).serialize
    )
    

async def quiz_user_sprints(request: HttpRequest, quiz: str, user: str):
    try:
        quiz = await MobileQuizModel.objects.aget(uuid = quiz)
        user = await MobileUserModel.objects.aget(uuid = user)
    except (
        ValidationError, 
        MobileUserModel.DoesNotExist, MobileQuizModel.DoesNotExist
    ):
        return CustomJsonResponse(status=404)
    
    return paginate(
        request = request,
        side_data= {
            "quiz": SN("$preview").serialize(quiz),
            "user": SN("$preview").serialize(user),
        },
        data = (
            MobileQuizUserSprintModel.objects
                .order_by('-finished_at')
        ),
        serializer = SN("$public").serialize
    )

    
async def quiz_sprint_answers(request: HttpRequest, uuid: str):
    try:
        model = await MobileQuizUserSprintModel.objects.aget(
            uuid = uuid,
        )
    except (ValidationError, MobileQuizUserSprintModel.DoesNotExist):
        return CustomJsonResponse({}, status=404)
    
    return paginate(
        request = request,
        side_data={
            "sprint": SN("$public").serialize(model)
        },
        data = (
            MobileQuizUserAnswerModel.objects
                .annotate(
                    is_finished = ~Q(status = MobileQuizUserAnswerModel.Status.ON_VERIFICATION),
                )
                .filter(
                    sprint = model,
                )
                .order_by("is_finished", '-updated_at')
        ),
        serializer = SN("$public").serialize
    )
