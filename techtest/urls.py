from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("regions/", include('regions.urls')),
    path("articles/", include('articles.urls')),
    path("authors/", include('authors.urls')),
]
