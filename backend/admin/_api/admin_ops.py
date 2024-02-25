from django.http import HttpRequest

from mobile.utils import ResponseType, typed_response
from utils.web import CustomJsonResponse
from admin.models import AdminPermission
from admin.conf import config


async def super_ops(request: HttpRequest):
    if(
        hasattr(request, "_session") 
        and not request._session.has_permission(AdminPermission.OWNER)
    ):
        return CustomJsonResponse(status=403)
    
    if "password" in request.POST:
        password = request.POST.get("password")
        if password:
            async with config as data:
                data['password'] = password
            
    return CustomJsonResponse(status=200)


async def logout(request: HttpRequest):
    await request._session.adelete()
    return typed_response(ResponseType.OKAY)
