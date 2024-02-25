from django.http import HttpRequest
from uuid import uuid4
import pendulum

from mobile.models import MobileNewsModel, MobileUserModel
from utils import SN
from utils.web import paginate, wrap_search, CustomJsonResponse
from cdn.utils import get_file_url


async def news_view(request: HttpRequest):
    view = paginate(
        request = request,
        response = False,
        data = wrap_search(
            request, ['name'], MobileNewsModel.objects.order_by('-created_at')).all(),
        serializer = SN("$public").serialize,
        side_data = False
    )
    
    if request.GET.get('p', None) == '1' and 'q' not in request.GET:
        dt = pendulum.now()
        
        birthday_query = (
            MobileUserModel.objects
                .filter(
                    status = MobileUserModel.Status.ACTIVE,
                    birthday__month = dt.month,
                    birthday__day = dt.day
                )
        )
        
        working_query = (
            MobileUserModel.objects
                .filter(
                    status = MobileUserModel.Status.ACTIVE,
                    working_at__month = dt.month,
                    working_at__day = dt.day,
                    working_at__year__lt = dt.year,
                )
        )
            
        if await birthday_query.aexists():
            async for user in birthday_query.all():
                name = user.full_name.partition(" ")[0]
                content_delta = [
                    { "insert": f"Today is {user.full_name} birthday." },
                    { "attributes": { "header": 2 }, "insert": "\n" },
                    { "insert": "Don't forget to congratulate him!" },
                    { "attributes": { "header": 3 }, "insert": "\n" },
                ]
                if user.description:
                    content_delta.extend([
                        { "insert": f"\nAbout {name}:" },
                        { "attributes": { "header": 2 }, "insert": "\n" },
                        { "insert": user.description },
                        { "attributes": { "header": 3 }, "insert": "\n" },
                    ])
                    
                view.insert(0, {
                    'uuid': str(uuid4()),
                    'image': get_file_url("/static/media_defaults/birthday.jpg")(user.avatar),
                    'name': f'Happy birthday, {name}!!!',
                    'content': content_delta,
                    'created_at': dt
                })
        
        if await working_query.aexists():
            async for user in working_query.all():
                name = user.full_name.partition(" ")[0]
                year_count = dt.year - user.working_at.year
                content_delta = [
                    { "insert": f"Today is {user.full_name} working anniversary." },
                    { "attributes": { "header": 2 }, "insert": "\n" },
                    { "insert": f"Work with us has been going on for {year_count} year\nDon't forget to congratulate him!" },
                    { "attributes": { "header": 3 }, "insert": "\n" },
                ]
                
                view.insert(0, {
                    'uuid': str(uuid4()),
                    'image': get_file_url("/static/media_defaults/anniversary.jpg")(user.avatar),
                    'name': f'Anniversary of {name} work!!!',
                    'content': content_delta,
                    'created_at': dt
                })
    
    return CustomJsonResponse(view)
