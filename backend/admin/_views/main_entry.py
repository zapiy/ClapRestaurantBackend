from django.http import HttpRequest
from django.shortcuts import render

from admin.conf import config
from admin.models import AdminSessionModel
from admin.middleware import apply_session_cookies, get_admin_session


async def main_entry(request: HttpRequest):
    if request.method == "POST":
        password = request.POST.get("password", None)
        if password is not None and config['password'] == password:
            session = AdminSessionModel()
            session.update_csrf_token()
            await session.asave(force_insert=True)
            request._session = session
            return await apply_session_cookies(
                request, render(
                    request, "admin/index.html", 
                    { 'PERMISSION': session.permission_level }
                ))
    
    session = await get_admin_session(request)
    if session is not None:
        return render(
            request, "admin/index.html", {
                'PERMISSION': session.permission_level,
            }
        )
        
    return render(request, "admin/auth.html")
