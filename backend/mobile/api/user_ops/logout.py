from django.http import HttpRequest

from mobile.models import MobileSessionModel
from mobile.app_messaging import AppMessaging
from mobile.utils import ResponseType, typed_response


async def logout(request: HttpRequest):
    session: MobileSessionModel = request._session
    await AppMessaging.logout_session(session)
    return typed_response(ResponseType.OKAY)
