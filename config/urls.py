from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_ratelimit.decorators import ratelimit

admin_site = admin.site
admin_site.login = ratelimit(key="ip", rate="5/m", method="POST")(admin_site.login)

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin_site.urls),
    path("", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
