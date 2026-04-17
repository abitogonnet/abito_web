from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('visitas/', include('visitas.urls')),
]

if not settings.USE_S3:
    urlpatterns += [
        # Renderiza /media con almacenamiento local cuando no hay bucket externo.
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
