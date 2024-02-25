from django.http import HttpRequest

from middleware import wrap_middleware
from ..utils import ResponseType, typed_response
from .. import utils


def mobile_is_authenticated():
    async def middleware(request: HttpRequest, next):
        session = await utils.get_session_from_request(request)
        if (
            session is None 
            or session.status != session.Status.ACTIVE 
            or session.user_id is None
        ):
            return typed_response(ResponseType.RESTRICT)
        
        request._session = session
        request._user = session.user
        return await next()
    return wrap_middleware(middleware)
