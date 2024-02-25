from django.http import HttpRequest

from admin.models import AdminUserModel, AdminPermission
from utils.web import CustomJsonResponse
from utils.web.field_handlers import generate_admin_item_view


async def validate_access(request: HttpRequest, uuid: str):
    if(
        hasattr(request, "_session") 
        and not request._session.has_permission(AdminPermission.OWNER)
    ):
        return CustomJsonResponse(status=403)

moderator = generate_admin_item_view(AdminUserModel, before=validate_access)
