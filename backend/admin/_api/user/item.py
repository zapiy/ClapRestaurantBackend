from django.http import HttpRequest
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from textwrap import dedent
import pendulum

from third_party import GmailSender
from mobile.app_messaging import AppMessaging
from mobile.models import MobileUserModel, MobileQuizModel
from cdn.utils import process_file, FileType, ensure_recycle
from utils import SN, generate_token
from utils.web import CustomJsonResponse


async def user(request: HttpRequest, uuid: str):
    is_new = uuid == 'new'
    if is_new and request.method == 'POST':
        user = MobileUserModel()
    else:
        try:
            user = await MobileUserModel.objects.aget(uuid = uuid)
        except (MobileUserModel.DoesNotExist, ValidationError):
            return CustomJsonResponse(status=404)
    
    if request.method == "POST":
        if "op" in request.POST and not is_new:
            op = request.POST.get('op', None)
            if op == 'switch':
                user.status = (
                    MobileUserModel.Status.NEWBIE
                    if user.status == MobileUserModel.Status.LEAVE else
                    MobileUserModel.Status.LEAVE
                )
                if user.status == MobileUserModel.Status.LEAVE:
                    await AppMessaging.logout_user(user)
                    await user.quiz_sprints.all().adelete()
                        
                    await GmailSender.send_mail(
                        recipient=user.email,
                        title="[Clap]: Thanks for your work!",
                        text="You were fired, thanks for your work!"
                    )
                else:
                    user.working_at = pendulum.now()
                    if not (
                        await MobileQuizModel.objects
                            .filter(newbie_required = True)
                            .aexists()
                    ):
                        user.status = MobileUserModel.Status.ACTIVE
                        
                await user.asave(force_update=True)
            
        elif (is_new or user.status != MobileUserModel.Status.LEAVE):
            if "avatar" in request.FILES and not is_new:
                await ensure_recycle(user.avatar)
                user.avatar = await process_file(request.FILES['avatar'], FileType.IMAGE)
                await user.asave(force_update=True)
            else:
                data = SN("_public").parse(request.POST, user)
                if data:
                    if is_new:
                        if (
                            await MobileUserModel.objects
                                .filter(email__iexact = data.email)
                                .aexists()
                        ):
                            return CustomJsonResponse(status=406)
                        
                        password = generate_token(8)
                        user.password_hash = make_password(password)
                        
                        await GmailSender.send_mail(
                            recipient=user.email,
                            title="[Clap]: Welcome!",
                            text=dedent(f"""\
                                You have successfully registered in Clap!
                                Your password: {password}
                            """)
                        )
                        
                        if not (
                            await MobileQuizModel.objects
                                .filter(newbie_required = True)
                                .aexists()
                        ):
                            user.status = MobileUserModel.Status.ACTIVE
                        
                        await user.asave(force_insert=True)
                    else:
                        await user.asave(force_update=True)
                
                elif user.uuid is None:
                    return CustomJsonResponse(status=406)
    
    return CustomJsonResponse(SN("$public", "status").serialize(user))
