from marshmallow import validate
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load

from .models import Author


class AuthorSchema(Schema):
    class Meta(object):
        model = Author

    id = fields.Integer()
    first_name = fields.String(validate=validate.Length(max=100))
    last_name = fields.String(validate=validate.Length(max=100))

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        article, _ = Author.objects.update_or_create(
            id=data.pop("id", None), defaults=data
        )
        return article
