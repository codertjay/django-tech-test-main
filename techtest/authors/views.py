import json

from marshmallow import ValidationError

from techtest.authors.models import Author
from techtest.authors.schemas import AuthorSchema
from techtest.utils import json_response, verify_user_token

from django.views.generic import View


class AuthorListView(View):
    def get(self, request, *args, **kwargs):
        return json_response(AuthorSchema().dump(Author.objects.all(), many=True))

    def post(self, request, *args, **kwargs):
        try:
            # token login required
            if not verify_user_token(request):
                return json_response({"message": "Unauthorized"}, status=401)

            author = AuthorSchema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(AuthorSchema().dump(author), 201)


class AuthorView(View):

    def dispatch(self, request, author_id, *args, **kwargs):
        try:
            self.author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return json_response({"error": "No Author matches the given query"}, 404)
        self.data = request.body and dict(json.loads(request.body), id=self.author.id)
        return super(AuthorView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return json_response(AuthorSchema().dump(self.author))

    def put(self, request, *args, **kwargs):
        try:
            # token login required
            if not verify_user_token(request):
                return json_response({"message": "Unauthorized"}, status=401)

            self.author = AuthorSchema().load(self.data)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(AuthorSchema().dump(self.author))

    def delete(self, request, *args, **kwargs):
        # token login required
        if not verify_user_token(request):
            return json_response({"message": "Unauthorized"}, status=401)

        self.author.delete()
        return json_response()
