from django.http import HttpRequest
from django.core.exceptions import ValidationError

from mobile.models import MobileFoodCategoryModel, MobileFoodModel
from utils import SN
from utils.web import CustomJsonResponse, paginate
from django.db.models import Count


async def food_categories(request: HttpRequest):
    return CustomJsonResponse(
        SN("$public").serialize(
            MobileFoodCategoryModel.objects.filter(parent = None).all()
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
        side_data={
            "category": SN("$public").serialize(model),
        },
        request = request,
        data = MobileFoodModel.objects.filter(category = model).all(),
        serializer = SN("$public").serialize
    )
