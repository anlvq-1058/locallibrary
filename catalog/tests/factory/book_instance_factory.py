import factory
from faker import Faker
from .book_factory import BookFactory
from catalog.models import BookInstance
from .genre_factory import GenreFactory

class BookInstanceFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = BookInstance
  book = factory.SubFactory(BookFactory)
  imprint = '12'
  status = 'a'

