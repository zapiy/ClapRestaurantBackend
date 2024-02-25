from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.landing, name="landing"),
    path('admin/', include('admin._views')),
    path('@/api/admin/', include('admin._api')),
    path('@/api/mobile/', include('mobile.api')),
]

if settings.DEBUG:
    if settings.MEDIA_ROOT != '/':
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
