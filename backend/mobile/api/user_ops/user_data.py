from django.http import HttpRequest
from django.contrib.auth.hashers import make_password

from utils.web import CustomJsonResponse
from utils import SN, SNF
from middleware import allowed_methods
from mobile.models import MobileUserModel
from mobile.utils import ResponseType, typed_response
from cdn.utils import process_file, FileType, ensure_recycle
from .auth import PASSWORD_VALIDATE

DESCRIPTION_VALIDATE = SNF(str, null=True, limit=range(10, 1000))


@allowed_methods("GET", "POST")
async def user_data(request: HttpRequest):
    user: MobileUserModel = request._user
    
    if request.method == "POST":
        if "avatar" in request.FILES:
            await ensure_recycle(user.avatar)
            user.avatar = await process_file(request.FILES['avatar'], FileType.IMAGE)
            await user.asave(force_update=True)
            
        elif "password" in request.POST:
            password = SN.safe_get(request.POST, 'password', PASSWORD_VALIDATE)
            if password:
                user.password_hash = make_password(password)
                await user.asave(force_update=True)
                
        elif "description" in request.POST:
            description = SN.safe_get(request.POST, 'description', DESCRIPTION_VALIDATE)
            if description:
                user.description = description
                await user.asave(force_update=True)
        
        return typed_response(ResponseType.OKAY)
    
    return CustomJsonResponse({
        "is_newbie": user.status == MobileUserModel.Status.NEWBIE,
        **SN("$public").serialize(user),
    })
