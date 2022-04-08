import json

from django.views.generic import View
from marshmallow import ValidationError

from techtest.utils import json_response
from techtest.users.models import User
from .schemas import UserSignUpSchema


class UserSignupView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print(data)
            if User.objects.filter(email=data.get('email')):
                return json_response({'message': 'Email already exists'}, status=400)
            if data.get('password') != data.get('confirm_password'):
                return json_response({"message": "Both password are not equal"}, 400)
            self.user = UserSignUpSchema().load(data)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(UserSignUpSchema().dump(self.user), status=200)


class UserLoginView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = User.objects.filter(email=data.get('email')).first()
            if not user:
                return json_response({'message': "User does not exist"}, status=400)
            is_user = user.check_password(data.get('password'))
            if not is_user:
                return json_response({'message': "Incorrect credentials"}, status=400)
            return json_response(UserSignUpSchema().dump(user))
        except Exception as a:
            return json_response(a, status=400)
