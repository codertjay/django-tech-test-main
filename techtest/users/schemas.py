import uuid

from marshmallow import validate
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load

from .models import User


class UserSignUpSchema(Schema):
    class Meta(object):
        model = User

    email = fields.Email()
    password = fields.String(validate=validate.Length(max=50), load_only=True)
    confirm_password = fields.String(validate=validate.Length(max=50))
    token = fields.String()

    @post_load
    def create(self, data, *args, **kwargs):
        user = User()
        user.email = data.get('email')
        user.set_password(data.get('password'))
        # user.id = uuid.uuid4
        user.save()
        return user
