from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.db.models import Count

from utils import SN, SNF
from mobile.app_messaging import AppMessaging
from mobile.models import MobileFoodCategoryModel, MobileFoodModel
from utils.web.field_handlers import generate_admin_item_view, FieldType


async def food_side_processing(request: HttpRequest, model: MobileFoodModel) -> bool:
    if hasattr(model, 'category') and model.category is not None:
        return False
    
    category = SN.safe_get(request.POST, "category", SNF(str, null=True, validate=lambda v: len(v) in range(34, 40)))
    if not category:
        return True
    
    try:
        model.category = (
            await MobileFoodCategoryModel.objects
                .annotate(child_count = Count('children'))
                .aget(uuid = category, child_count = 0)
        )
    except (ValidationError, MobileFoodCategoryModel.DoesNotExist):
        return True


food = generate_admin_item_view(
    MobileFoodModel,
    side_processing=food_side_processing,
    on_added=AppMessaging.new_food,
    extra_mapping={
        "image": FieldType.IMAGE,
        "content": FieldType.RICH,
    },
)
