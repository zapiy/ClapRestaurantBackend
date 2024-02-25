from django.http import HttpRequest

from mobile.models import MobileUserModel
from utils import SN
from utils.web import paginate, wrap_search


async def users(request: HttpRequest):
    return paginate(
        request = request,
        data = wrap_search(
            request, ['full_name', "email"], 
            MobileUserModel.objects.order_by('-working_at')).all(),
        serializer = SN("$public", "status").serialize
    )
