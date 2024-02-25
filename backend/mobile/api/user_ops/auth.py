from django.http import HttpRequest
from django.contrib.auth.hashers import make_password, check_password
from textwrap import dedent
import logging

from third_party import GmailSender
from middleware import allowed_methods
from utils import SN, SNF, generate_token
from mobile.app_messaging import AppMessaging
from mobile.utils import ResponseType, typed_response
from mobile.models import MobileUserModel, MobileSessionModel
from mobile.utils import RegexPack, get_session_from_request

logger = logging.getLogger("mobile_auth")
logger.setLevel(logging.DEBUG)

FCM_VALIDATE = SNF(str, validate=lambda v: len(v) in range(100, 250))
EMAIL_VALIDATE = SNF(str, validate=lambda v: len(v) in range(8, 120) and bool(RegexPack.EMAIL_REGEX.match(v)))
PASSWORD_VALIDATE = SNF(str, limit=range(7, 30))
LOGIN_FORM = SN(
    email = EMAIL_VALIDATE,
    password = PASSWORD_VALIDATE,
    fcm_token = FCM_VALIDATE
)

@allowed_methods("GET", "POST")
async def auth(request: HttpRequest):
    operation = request.GET.get("op", None)
    
    if operation == "login":
        form = LOGIN_FORM.parse(request.POST)
        
        if not form:
            return typed_response(ResponseType.INVALID_FIELDS, status=409)
        
        try:
            user = await MobileUserModel.objects.aget(email__iexact = form.email)
        except MobileUserModel.DoesNotExist:
            return typed_response(ResponseType.INVALID_FIELDS, status=409)
        
        if not check_password(form.password, user.password_hash):
            return typed_response(ResponseType.INVALID_FIELDS, status=409)
        elif user.status == MobileUserModel.Status.LEAVE:
            return typed_response(ResponseType.BLOCKED, status=403)
        
        session = MobileSessionModel(
            user = user,
            status = MobileSessionModel.Status.ACTIVE,
            fcm_token = form.fcm_token
        )
        await AppMessaging.login_session(session)
        await session.asave(force_insert=True)
        
        logger.debug(f"Auth with email: {user.email}")
        return typed_response(ResponseType.LOGGED_IN, data = { "bearer": session.auth_token })
    
    elif operation == "restore":
        email = SN.safe_get(request.POST, 'email', EMAIL_VALIDATE)
        
        if not email:
            return typed_response(ResponseType.INVALID_FIELDS, status=409)
        
        try:
            user = await MobileUserModel.objects.aget(email__iexact = email)
        except MobileUserModel.DoesNotExist:
            return typed_response(ResponseType.INVALID_FIELDS, status=409)
        
        if user.status == MobileUserModel.Status.LEAVE:
            return typed_response(ResponseType.BLOCKED, status=403)
        
        await AppMessaging.logout_user(user)
        
        password = generate_token(8)
        user.password_hash = make_password(password)
        
        await GmailSender.send_mail(
            recipient=user.email,
            title="[Clap]: Password restore",
            text=dedent(f"""\
                Your password has been successfully reset!
                Your password: {password}
            """)
        )
        
        await user.asave(force_update=True)
        return typed_response(ResponseType.OKAY)
    
    elif "Authorization" in request.headers:
        session = await get_session_from_request(request)
        if session is None or session.status == session.Status.EXPIRED:
            return typed_response(ResponseType.SESSION_EXPIRED, status=401)
        
        if operation == "validate":
            if session is None or session.status != session.Status.ACTIVE:
                return typed_response(ResponseType.SESSION_EXPIRED, status=401)
            elif session.user.status == session.user.Status.LEAVE:
                return typed_response(ResponseType.BLOCKED)
            
            await session.asave(force_update=True)
            return typed_response(ResponseType.LOGGED_IN)
    
    return typed_response(ResponseType.UNKNOWN_OPERATION, status=406)
