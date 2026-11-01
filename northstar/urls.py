from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("services/", include("services.urls")),
    path("projects/", include("projects.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    from django.views.generic import TemplateView

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Preview the custom error pages locally. Django only uses them when DEBUG is False.
    urlpatterns += [
        path("__preview/404/", TemplateView.as_view(template_name="404.html")),
        path("__preview/500/", TemplateView.as_view(template_name="500.html")),
    ]
