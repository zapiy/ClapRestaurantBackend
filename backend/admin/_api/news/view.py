from django.http import HttpRequest

from mobile.models import MobileNewsModel
from utils import SN
from utils.web import paginate


async def news_view(request: HttpRequest):
    return paginate(
        request = request,
        data = MobileNewsModel.objects.order_by('-created_at').all(),
        serializer = SN("$public").serialize
    )
