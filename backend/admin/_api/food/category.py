from django.core.exceptions import ValidationError
from django.http import HttpRequest

from mobile.models import MobileFoodCategoryModel
from utils import SN, SNF
from utils.web import CustomJsonResponse
from cdn.utils import process_file, FileType, ensure_recycle


async def food_category(request: HttpRequest, uuid: str):
    if uuid == 'new':
        if request.method != 'POST':
            return CustomJsonResponse({}, status=404)
        model = MobileFoodCategoryModel()
    else:
        try:
            model = await MobileFoodCategoryModel.objects.aget(uuid = uuid)
        except (ValidationError, MobileFoodCategoryModel.DoesNotExist):
            return CustomJsonResponse({}, status=404)
    
    if request.method == "DELETE":
        if "uuid" in request.POST:
            if (
                request.POST["uuid"] == str(model.uuid) 
                and (await model.children.acount()) == 0
                and (await model.foods.acount()) == 0
            ):
                await ensure_recycle(model.image)
                await model.adelete()
                return CustomJsonResponse({}, status=200)
            return CustomJsonResponse({}, status=406)
            
    elif request.method == "POST":
        data = SN("_public").parse(request.POST, model)
        if uuid == 'new':
            if data:
                parent = SN.safe_get(request.POST, "parent", SNF(str, null=True, validate=lambda v: len(v) in range(34, 40)))
                if parent:
                    try:
                        data.parent = await MobileFoodCategoryModel.objects.aget(uuid = parent)
                        if (
                            data.parent.parent_id is not None 
                            or (await data.parent.foods.acount()) > 0
                        ):
                            return CustomJsonResponse({}, status = 406)
                    except (ValidationError, MobileFoodCategoryModel.DoesNotExist):
                        return CustomJsonResponse({}, status=404)
                    
                await data.asave(force_insert=True)
            else:
                return CustomJsonResponse({}, status = 406)
        
        if "image" in request.FILES:
            await ensure_recycle(data.image)
            data.image = await process_file(request.FILES['image'], FileType.IMAGE)
        
        if data:
            await data.asave(force_update=True)
    
    return CustomJsonResponse(SN("$public").serialize(model))
