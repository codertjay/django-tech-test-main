from django.urls import path

from techtest.authors.views import AuthorListView, AuthorView

app_name = 'author'
urlpatterns = [
    path("", AuthorListView.as_view(), name='author-list'),
    path("<int:author_id>/", AuthorView.as_view(), name="author"),

]
