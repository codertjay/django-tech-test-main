import json

from django.test import TestCase, Client
from django.urls import reverse

from techtest.regions.models import Region
from techtest.users.models import User


class RegionListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("regions:regions-list")
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.user_token = User.objects.create(email='test@gmail.com', password='Password12')

    @property
    def login_client(self):
        client = Client(HTTP_TOKEN=self.user_token.token)
        return client

    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            [
                {
                    "id": self.region_1.id,
                    "code": "AL",
                    "name": "Albania",
                },
                {
                    "id": self.region_2.id,
                    "code": "UK",
                    "name": "United Kingdom",
                },
            ],
        )

    def test_creates_new_region(self):
        payload = {
            "code": "US",
            "name": "United States of America",
        }
        response = self.login_client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        region = Region.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(region)
        self.assertEqual(Region.objects.count(), 3)
        self.assertDictEqual(
            {
                "id": region.id,
                "code": "US",
                "name": "United States of America",
            },
            response.json(),
        )


class RegionViewTestCase(TestCase):
    def setUp(self):
        self.region = Region.objects.create(code="AL", name="Albania")
        self.url = reverse("regions:region", kwargs={"region_id": self.region.id})
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
                "id": self.region.id,
                "code": "AL",
                "name": "Albania",
            },
        )

    def test_updates_region(self):
        payload = {
            "id": self.region.id,
            "code": "US",
            "name": "United States of America",
        }
        response = self.login_client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        region = Region.objects.filter(id=self.region.id).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(region)
        self.assertEqual(Region.objects.count(), 1)
        self.assertDictEqual(
            {
                "id": region.id,
                "code": "US",
                "name": "United States of America",
            },
            response.json(),
        )

    def test_removes_region(self):
        response = self.login_client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Region.objects.count(), 0)
