import factory
from catalog.models import Genre

class GenreFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Genre

  name = 'abc abc'
