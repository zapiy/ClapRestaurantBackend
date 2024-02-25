from django.http import HttpRequest
from django.shortcuts import redirect


async def landing(request: HttpRequest):
    return redirect('admin:main', permanent=True)
