from django.http import HttpRequest

from admin.models import AdminUserModel, AdminPermission
from utils import SN
from utils.web import paginate, wrap_search, CustomJsonResponse


async def moderator_view(request: HttpRequest):
    if(
        hasattr(request, "_session") 
        and not request._session.has_permission(AdminPermission.OWNER)
    ):
        return CustomJsonResponse(status=403)
    
    return paginate(
        request = request,
        data = wrap_search(
            request, ['key_name'], 
            AdminUserModel.objects.order_by('-created_at')).all(),
        serializer = SN("$public").serialize
    )
