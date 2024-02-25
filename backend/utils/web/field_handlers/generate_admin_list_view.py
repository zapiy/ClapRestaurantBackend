from typing import Awaitable, Callable, List, Optional, Type, Union
from django.http import HttpRequest
from django.db.models import Model, QuerySet

from utils import SN
from utils.web import CustomJsonResponse
from utils.web import paginate as web_paginator, wrap_search


def generate_simple_admin_list_view(
    model_type: Type[Model],
    *,
    serialize_mapping: SN,
    relative_to: Optional[Union[Model, Callable[[QuerySet], Awaitable[QuerySet]]]] = None,
    paginate: bool = False,
    order_by: Optional[Union[str, List[str]]] = None,
    search_by: Optional[List[str]] = None
):
    async def handler(request: HttpRequest, uuid: str = None):
        query = model_type.objects
        
        if order_by:
            if isinstance(order_by, str):
                query = query.order_by(order_by)
            elif isinstance(order_by, list):
                query = query.order_by(*order_by)
        
        if search_by:
            query = wrap_search(request, search_by, query)
        
        query = query.all()
        
        if paginate:
            return web_paginator(
                request = request,
                data = query.all(),
                serializer = serialize_mapping.serialize,
                side_data=True
            )
        return CustomJsonResponse(serialize_mapping.serialize(query.all()))
    return handler