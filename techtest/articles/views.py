import json

from marshmallow import ValidationError
from django.views.generic import View

from techtest.articles.models import Article
from techtest.articles.schemas import ArticleSchema
from techtest.utils import json_response, verify_user_token


class ArticlesListView(View):
    def get(self, request, *args, **kwargs):
        return json_response(ArticleSchema().dump(Article.objects.all(), many=True))

    def post(self, request, *args, **kwargs):
        try:
            # token login required
            if not verify_user_token(request):
                return json_response({"message": "Unauthorized"}, status=401)

            article = ArticleSchema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        except Exception as e:
            return json_response({"message": "An error occurred", "error": str(e)}, 400)
        return json_response(ArticleSchema().dump(article), 201)


class ArticleView(View):
    def dispatch(self, request, article_id, *args, **kwargs):
        try:
            self.article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return json_response({"error": "No Article matches the given query"}, 404)
        self.data = request.body and dict(json.loads(request.body), id=self.article.id)
        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return json_response(ArticleSchema().dump(self.article))

    def put(self, request, *args, **kwargs):
        try:
            # token login required
            if not verify_user_token(request):
                return json_response({"message": "Unauthorized"}, status=401)

            self.article = ArticleSchema().load(self.data)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(ArticleSchema().dump(self.article))

    def delete(self, request, *args, **kwargs):
        # token login required
        if not verify_user_token(request):
            return json_response({"message": "Unauthorized"}, status=401)
        self.article.delete()
        return json_response({'message': 'Successfully deleted article'}, status=200)
