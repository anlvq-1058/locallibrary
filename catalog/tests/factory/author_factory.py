import factory
from faker import Faker

from catalog.models import Author


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    first_name = Faker().name()
    last_name = Faker().name()
    date_of_birth = Faker().date()
