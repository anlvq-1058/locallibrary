from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from catalog.models import Book, Author, BookInstance, Genre

class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death']

class BooksSerializer(serializers.ModelSerializer):
  author = AuthorSerializer()
  hello = serializers.SerializerMethodField()
  class Meta:
    model = Book
    fields = ['id', 'title', 'genre', 'author', 'genre', 'hello']
  def get_hello(self, obj):
    return "hello id: %i" % obj.pk


class BookInstanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = BookInstance
    fields = ['id', 'book', 'imprint', 'due_back', 'status', 'borrower']
