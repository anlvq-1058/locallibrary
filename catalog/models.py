from django.db import models
from django.urls import reverse
import uuid
from .utils.constants import LOAN_STATUS
from django.utils.translation import gettext_lazy as _

class Genre(models.Model):
  """Model representing a book genre."""
  name = models.CharField(max_length=200, help_text=_('DescriptionBook'))
  def __str__(self):
    """String for representing the Model object."""
    return self.name

class Book(models.Model):
  """Model representing a book (but not a specific copy of a book)."""
  title = models.CharField(max_length=200)
  author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
  summary = models.TextField(max_length=1000, help_text='')
  isbn = models.CharField('ISBN', max_length=13, unique=True,help_text=_('IsbnNumber'))
  genre = models.ManyToManyField(Genre, help_text=_('SelectGenre'))

  def __str__(self):
    """String for representing the Model object."""
    return self.title

  def get_absolute_url(self):
    """Returns the url to access a detail record for this book."""
    return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
  """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('UniqueID'))
  book = models.ForeignKey('Book', on_delete=models.RESTRICT)
  imprint = models.CharField(max_length=200)
  due_back = models.DateField(null=True, blank=True)
  status = models.CharField(
                            max_length=1,
                            choices=LOAN_STATUS,
                            blank=True,
                            default='m',
                            help_text=_('BookAvailability'),
                            )
  class Meta:
    ordering = ['due_back']
  def __str__(self):
    """String for representing the Model object."""
    return f'{self.id} ({self.book.title})'

class Author(models.Model):
  """Model representing an author."""
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField(null=True, blank=True)
  date_of_death = models.DateField('Died', null=True, blank=True)
  class Meta:
    ordering = ['last_name', 'first_name']
  def get_absolute_url(self):
    """Returns the url to access a particular author instance."""
    return reverse('author-detail', args=[str(self.id)])
  def __str__(self):
    """String for representing the Model object."""
    return f'{self.last_name}, {self.first_name}'
