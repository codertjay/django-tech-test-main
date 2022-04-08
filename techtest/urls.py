from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("regions/", include('techtest.regions.urls')),
    path("articles/", include('techtest.articles.urls')),
    path("authors/", include('techtest.authors.urls')),
    path("users/", include('techtest.users.urls')),
]
