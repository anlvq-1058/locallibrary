import factory
from catalog.models import Book
from .author_factory import AuthorFactory
from faker import Faker

class BookFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Book

  title = Faker().name()
  summary = Faker().sentence(nb_words=10)
  isbn = Faker().sbn9()
  author = factory.SubFactory(AuthorFactory)

  @factory.post_generation
  def genre(self, create, extracted, **kwargs):
    if not create or not extracted:
      return
    self.genre.add(*extracted)
