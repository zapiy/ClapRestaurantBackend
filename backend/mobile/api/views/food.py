from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.db.models import Count

from mobile.models import MobileFoodCategoryModel, MobileFoodModel
from utils.web import paginate, wrap_search, CustomJsonResponse
from utils import SN


async def food_categories(request: HttpRequest):
    return CustomJsonResponse(
        SN("$public").serialize(
            wrap_search(request, ['name'], MobileFoodCategoryModel.objects.filter(parent = None)).all()
        )
    )


async def foods_of_category(request: HttpRequest, uuid: str):
    try:
        model = (
            await MobileFoodCategoryModel.objects
                .annotate(child_count = Count('children'))
                .aget(uuid = uuid, child_count = 0)
        )
    except (ValidationError, MobileFoodCategoryModel.DoesNotExist):
        return CustomJsonResponse({}, status=404)
    
    return paginate(
        request = request,
        data = wrap_search(
            request, ['name'], MobileFoodModel.objects.filter(category = model)).all(),
        serializer = SN("$public").serialize,
        side_data = False
    )
