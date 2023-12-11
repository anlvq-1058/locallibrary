import factory
from catalog.models import Author
from faker import Faker

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    first_name = Faker().name()
    last_name = Faker().name()
    date_of_birth = Faker().date()
