import json

from django.test import TestCase, Client
from django.urls import reverse

from techtest.authors.models import Author
from techtest.users.models import User


class AuthorListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("author:author-list")
        self.author_1 = Author.objects.create(first_name="Favour", last_name="Festus")
        self.author_2 = Author.objects.create(first_name="ThankGod", last_name="Festus")
        self.user_token = User.objects.create(email='test@gmail.com', password='Password12')

    @property
    def login_client(self):
        client = Client(HTTP_TOKEN=self.user_token.token)
        return client

    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertCountEqual(
            response.json(),
            [
                {'first_name': 'Favour', 'last_name': 'Festus', 'id': self.author_1.id},
                {'first_name': 'ThankGod', 'last_name': 'Festus', 'id': self.author_2.id}
            ]
        )

    def test_creates_new_author(self):
        payload = {
            "first_name": "David",
            "last_name": "Daniel",
        }
        response = self.login_client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(author)
        self.assertEqual(Author.objects.count(), 3)
        self.assertDictEqual(
            {
                "id": author.id,
                "first_name": "David",
                "last_name": "Daniel",
            },
            response.json(),
        )


class AuthorViewTestCase(TestCase):
    def setUp(self):
        self.first_name = 'Favour'
        self.last_name = 'Afenikhena'
        self.author = Author.objects.create(first_name=self.first_name, last_name=self.last_name)
        self.url = reverse("author:author", kwargs={"author_id": self.author.id})
        self.user_token = User.objects.create(email='test@gmail.com', password='Password12')

    @property
    def login_client(self):
        client = Client(HTTP_TOKEN=self.user_token.token)
        return client

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {
                "id": self.author.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
            },
        )

    def test_updates_author(self):
        payload = {
            "id": self.author.id,
            "first_name": "Mike",
            "last_name": "Afenikhena",
        }
        response = self.login_client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.filter(id=self.author.id).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(author)
        self.assertEqual(Author.objects.count(), 1)
        self.assertDictEqual(
            {
                "id": author.id,
                "first_name": "Mike",
                "last_name": "Afenikhena",
            },
            response.json(),
        )

    def test_removes_author(self):
        response = self.login_client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Author.objects.count(), 0)
