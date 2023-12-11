import datetime
from django.test import TestCase
from importlib import reload
from catalog.models import Author, Book, BookInstance
from .factory.book_factory import BookFactory
from .factory.genre_factory import GenreFactory
from .factory.author_factory import AuthorFactory
from .factory.book_instance_factory import BookInstanceFactory

class AuthorModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    AuthorFactory()

  def test_first_name_label(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('first_name').verbose_name
    self.assertEqual(field_label, 'first name')

  def test_date_of_death_label(self):
    author = Author.objects.get(id=1)
    field_label = author._meta.get_field('date_of_death').verbose_name
    self.assertEqual(field_label, 'Died')

  def test_first_name_max_length(self):
    author = Author.objects.get(id=1)
    max_length = author._meta.get_field('first_name').max_length
    self.assertEqual(max_length, 100)

  def test_object_name_is_last_name_comma_first_name(self):
    author = Author.objects.get(id=1)
    expected_object_name = f'{author.last_name}, {author.first_name}'
    self.assertEqual(str(author), expected_object_name)

  def test_get_absolute_url(self):
    author = Author.objects.get(id=1)
    self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

class BookModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.genre1 = GenreFactory()
    cls.genre2 = GenreFactory()
    BookFactory.create(genre=(cls.genre1, cls.genre2))

  def test_get_absolute_url(self):
    book = Book.objects.first()
    self.assertEqual(book.get_absolute_url(), f'/catalog/book/{book.id}')

  def test_display_genre(self):
    book = Book.objects.first()
    self.assertEqual(book.display_genre(), f'{self.genre1}, {self.genre2}')

  def test_display_genre_max_3_item(self):
    book = Book.objects.first()
    genre3 = GenreFactory()
    genre4 = GenreFactory()
    book.genre.add(genre3, genre4)
    self.assertEqual(book.display_genre(), f'{self.genre1}, {self.genre2}, {genre3}')

class BookInstanceModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.book_instance = BookInstanceFactory()
  def test_is_overdue(self):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    self.book_instance.due_back = yesterday
    self.book_instance.save()
    self.assertTrue(self.book_instance.is_overdue)
