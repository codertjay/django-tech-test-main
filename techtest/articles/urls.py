from django.urls import path

from .views import ArticleView, ArticlesListView

app_name = 'articles'
urlpatterns = [
    path("", ArticlesListView.as_view(), name="articles-list"),
    path("<int:article_id>/", ArticleView.as_view(), name="article"),
]
