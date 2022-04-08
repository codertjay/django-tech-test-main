import json

from django.test import TestCase
from django.urls import reverse

from techtest.users.models import User


class UserTestCase(TestCase):

    def setUp(self):
        self.login_url = reverse("users:user-login")
        self.signup_url = reverse("users:user-signup")
        self.user = User.objects.create(
            email='codertjay1@gmail.com',
            password='Password12',
        )

    def test_signup_and_login(self):
        email = 'favourdeveloper@gmail.com'
        password = 'password_@'
        payload = {
            'email': email,
            'password': password,
            'confirm_password': password
        }
        signup_response = self.client.post(self.signup_url, data=json.dumps(payload), content_type="application/json")
        print(signup_response.json())
        self.assertNotEqual(signup_response.status_code, 400)
        self.assertEqual(signup_response.status_code, 200)
        # login user
        payload = {
            'email': email,
            'password': password
        }
        login_response = self.client.post(self.login_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(login_response.status_code, 200)

        # login user with wrong password
        payload = {
            'email': email,
            'password': 'wrongpassword'
        }
        login_response = self.client.post(self.login_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(login_response.status_code, 400)

    def test_wrong_password_signup(self):
        email = 'favourdeveloper@gmail.com'
        password = 'password_@'
        payload = {
            'email': email,
            'password': password,
            'confirm_password': 'passwordaa',
        }
        signup_response = self.client.post(self.signup_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(signup_response.status_code, 400)
