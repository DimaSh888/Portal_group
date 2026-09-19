from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portal_group.urls")),
    path("forum/", include("forum.urls")),
]
