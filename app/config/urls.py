from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('reset/', include('reset.urls', namespace='reset')),
    path('hikvisionadmin/', admin.site.urls),
    path('', include('user.urls', namespace='user')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
