import django, os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techtest.settings")
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", ".."))
django.setup()

from techtest.articles.models import Article
from techtest.regions.models import Region
from techtest.users.models import User
from techtest.authors.models import Author
from django.core import management

# Make Migrations
management.call_command('makemigrations', no_input=True)
# Migrate
management.call_command("migrate", no_input=True)

# Flush Database
management.call_command('flush', no_input=True)
# Seed
user = User()
user.email = email = 'codertjay@gmail.com'
user.set_password('MyPassword')
user.save()
author = Author.objects.create(first_name='favour', last_name='Afenikhena')
Article.objects.create(title="Fake Article", content="Fake Content", author=author).regions.set(
    [
        Region.objects.create(code="AL", name="Albania"),
        Region.objects.create(code="UK", name="United Kingdom"),
    ]
)
Article.objects.create(title="Fake Article", content="Fake Content", author=author)
Article.objects.create(title="Fake Article", content="Fake Content", author=author)
Article.objects.create(title="Fake Article", content="Fake Content", author=author)
Article.objects.create(title="Fake Article", content="Fake Content", author=author).regions.set(
    [
        Region.objects.create(code="AU", name="Austria"),
        Region.objects.create(code="US", name="United States of America"),
    ]
)
