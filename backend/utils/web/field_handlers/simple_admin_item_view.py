from typing import Awaitable, Callable, Dict, Optional, Type
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.db.models import Model

from utils import SN
from utils.web import CustomJsonResponse
from cdn.utils import ensure_recycle
from .handle_post_fields import handle_post_fields, FieldType


def generate_admin_item_view(
    model_type: Type[Model],
    *,
    serialize_mapping = SN('$public'),
    before: Callable[[HttpRequest, str], Awaitable[Optional[HttpResponse]]] = None,
    can_delete: bool = True,
    side_processing: Callable[[HttpRequest, Model], Awaitable[bool]] = None,
    parse_mapping: Optional[SN] = SN('_public'),
    extra_mapping: Dict[str, FieldType] = None,
    on_added: Callable[[Model], Awaitable] = None,
    on_deleted: Callable[[Model], Awaitable] = None,
):
    can_post = (parse_mapping or extra_mapping)
    async def handler(request: HttpRequest, uuid: str):
        if before is not None:
            before_resp = await before(request, uuid)
            if before_resp is not None:
                return before_resp
        
        is_new = uuid == 'new'        
        if is_new:
            if not can_post or request.method not in ["POST", "GET"]:
                return CustomJsonResponse(status=404)
            
            model = model_type()
            if request.method == "GET":
                model.uuid = "new"
        else:
            try:
                model = await model_type.objects.aget(uuid = uuid)
            except (ValidationError, model_type.DoesNotExist):
                return CustomJsonResponse(status=404)

        if (
            can_delete
            and request.method == "DELETE" 
            and not is_new
            and "uuid" in request.POST
        ):
            if request.POST["uuid"] == str(model.uuid):
                if extra_mapping:
                    for key, type in extra_mapping.items():
                        if type == FieldType.IMAGE:
                            await ensure_recycle(getattr(model, key))
                        
                await model.adelete()
                if on_deleted:
                    await on_deleted(model)
                    
                return CustomJsonResponse(status=200)
            return CustomJsonResponse(status=406)
        
        elif can_post and request.method == "POST":
            if await handle_post_fields(
                request, model, 
                mapping=parse_mapping, 
                extra=extra_mapping,
                side_processing=side_processing
            ):
                return CustomJsonResponse(status=406)
            
            if is_new:
                await model.asave(force_insert=True)
                if on_added:
                    await on_added(model)
            else:
                await model.asave(force_update=True)

        return CustomJsonResponse(serialize_mapping.serialize(model))

    return handler
