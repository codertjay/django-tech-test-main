import json

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from techtest.articles.models import Article
from techtest.authors.models import Author
from techtest.regions.models import Region
from techtest.users.models import User


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("articles:articles-list")
        self.article_1 = Article.objects.create(title="Fake Article 1")

        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")

        self.author_1 = Author.objects.create(first_name='Mark', last_name='Zuck')
        self.author_2 = Author.objects.create(first_name='Bill', last_name='Gates')
        self.article_2 = Article.objects.create(
            title="Fake Article 2", content="Lorem Ipsum", author=self.author_2
        )
        self.article_2.regions.set([self.region_1, self.region_2])

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
                    'title': 'Fake Article 1',
                    'id': self.article_1.id,
                    'content': '',
                    'author': {},
                    'regions': []
                },
                {
                    'title': 'Fake Article 2',
                    'id': self.article_2.id,
                    'content': 'Lorem Ipsum',
                    'author': {'last_name': 'Gates', 'first_name': 'Bill', 'id': self.author_2.id},
                    'regions': [
                        {'code': 'AL', 'id': self.region_1.id, 'name': 'Albania'},
                        {'code': 'UK', 'id': self.region_2.id, 'name': 'United Kingdom'}
                    ]}
            ]
        )

    def test_creates_new_article_with_regions(self):
        payload = {
            "title": "Fake Article 3",
            "content": "To be or not to be",
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"code": "AU", "name": "Austria"},
            ],
        }
        response = self.login_client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 2)
        self.assertDictEqual(
            {'author': {}, 'content': 'To be or not to be', 'title': 'Fake Article 3', 'id': article.id,
             'regions': [
                 {'name': 'United States of America',
                  'id': regions.all()[0].id,
                  'code': 'US'},
                 {'name': 'Austria',
                  'id': regions.all()[1].id,
                  'code': 'AU'}
             ]
             },
            response.json(),
        )

    def test_create_new_article_with_author(self):
        payload = {
            "title": "Fake Article 3",
            "content": "To be or not to be",
            "regions": [],
            "author": {'last_name': 'Gates', 'first_name': 'Bill'}
        }
        response = self.login_client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        author = Author.objects.filter(article=article)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(article)
        self.assertEqual(author.count(), 1)
        self.assertDictEqual(
            {
                'author': {
                    'id': author.first().id,
                    'last_name': 'Gates',
                    'first_name': 'Bill'
                },
                'content': 'To be or not to be', 'title': 'Fake Article 3', 'id': article.id,
                'regions': []
            },
            response.json(),
        )


class ArticleViewTestCase(TestCase):
    def setUp(self):
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.user_token = User.objects.create(email='test@gmail.com', password='Password12')

        self.author_1 = Author.objects.create(first_name='Favour', last_name='Festus')
        self.author_2 = Author.objects.create(first_name='Bill', last_name='Gates')

        self.article = Article.objects.create(title="Fake Article 1", author=self.author_1)

        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.article.regions.set([self.region_1, self.region_2])
        self.url = reverse("articles:article", kwargs={"article_id": self.article.id})

    @property
    def login_client(self):
        client = Client(HTTP_TOKEN=self.user_token.token)
        return client

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {'id': self.article.id, 'title': 'Fake Article 1',
             'regions': [{'name': 'Albania', 'id': self.region_1.id, 'code': 'AL'},
                         {'name': 'United Kingdom', 'id': self.region_2.id, 'code': 'UK'}],
             'author': {
                 'last_name': 'Festus',
                 'first_name': 'Favour',
                 'id': self.author_1.id},
             'content': ''},
        )

    def test_updates_article_and_regions(self):
        # Change regions
        payload = {
            "title": "Fake Article 1 (Modified)",
            "content": "To be or not to be here",
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"id": self.region_2.id},
            ],
        }
        response = self.login_client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.first()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 2)
        self.assertEqual(Article.objects.count(), 1)
        print(response.json())
        self.assertDictEqual(
            {'author': {'first_name': 'Favour', 'id': self.author_1.id, 'last_name': 'Festus'},
             'regions': [
                 {'code': 'UK', 'id': self.region_2.id, 'name': 'United Kingdom'},
                 {'code': 'US', 'id': regions.all()[1].id, 'name': 'United States of America'}],
             'id': article.id,
             'title': 'Fake Article 1 (Modified)', 'content': 'To be or not to be here'},
            response.json(),
        )
        # Remove regions
        payload["regions"] = []
        response = self.login_client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 0)
        print('json', response.json())

        self.assertDictEqual(
            {'id': article.id,
             'content': 'To be or not to be here',
             'regions': [],
             'title': 'Fake Article 1 (Modified)',
             'author': {'first_name': 'Favour', 'id': self.author_1.id, 'last_name': 'Festus'}
             },
            response.json(),
        )

    def test_update_articles_and_author(self):
        # Change author
        payload = {
            "title": "Fake Article 1 (Modified)",
            "content": "To be or not to be here",
            "regions": [
            ],
            'author': {'id': self.author_2.id}
        }
        response = self.login_client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(Article.objects.count(), 1)
        self.assertDictEqual(
            {'author': {'first_name': 'Bill', 'id': self.author_2.id, 'last_name': 'Gates'},
             'regions': [],
             'id': article.id,
             'title': 'Fake Article 1 (Modified)', 'content': 'To be or not to be here'},
            response.json(),
        )
        response = self.login_client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 0)

        self.assertDictEqual(
            {'id': article.id,
             'content': 'To be or not to be here',
             'regions': [],
             'title': 'Fake Article 1 (Modified)',
             'author': {'first_name': 'Bill', 'id': self.author_2.id, 'last_name': 'Gates'}
             },
            response.json(),
        )

    def test_removes_article(self):
        response = self.login_client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 0)
