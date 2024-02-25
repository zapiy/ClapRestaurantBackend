from django.http import HttpRequest
from django.db.models import Count, Q, Subquery, OuterRef, Value, IntegerField, CharField
from django.db.models.functions import Coalesce

from mobile.models import MobileUserModel, MobileQuizModel, MobileQuizUserSprintModel
from utils.web import paginate, wrap_search
from utils import SN


async def quizzes(request: HttpRequest):
    user: MobileUserModel = request._user
    
    sprint_query = (
        MobileQuizUserSprintModel.objects
            .filter(
                ~Q(status = MobileQuizUserSprintModel.Status.INCORRENT),
                user = user,
                quiz = OuterRef('uuid'),
            )
            .order_by("created_at")
    )
    
    query = (
        MobileQuizModel.objects
            .annotate(
                max_progress = Coalesce(Count('questions'), 0),
                current_progress = Coalesce(
                    Subquery(
                        sprint_query.values_list(Count('answers'))[:1]
                    ), 0,
                    output_field=IntegerField()
                ),
                status = Coalesce(
                    Subquery(
                        sprint_query.values_list('status')[:1]
                    ),
                    Value(MobileQuizUserSprintModel.Status.WHILE_TAKING),
                    output_field=CharField()
                ),
                is_finished = Q(status = MobileQuizUserSprintModel.Status.WHILE_TAKING)
            )
            .order_by('-is_finished', '-created_at')
    )
    
    if user.status == MobileUserModel.Status.NEWBIE:
        query = query.filter(newbie_required = True)
    
    return paginate(
        request = request,
        data = wrap_search(
            request, ['name'], query).all(),
        serializer = SN(
            "$public", "status",
            "current_progress", "max_progress"
        ).serialize,
        side_data = False
    )
    