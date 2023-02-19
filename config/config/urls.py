from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("config.apps.main.urls")),
    path('user/', include("config.apps.user.urls")),
    path('community/', include("config.apps.community.urls")),
    path('accounts/', include('allauth.urls')),
    path('closet/', include("config.apps.closet.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)