from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

@admin.register(Genre)

class AuthorAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
  fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

@admin.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
  model = BookInstance
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'display_genre')
  inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_filter = ('status', 'due_back')
  list_display = ('id', 'book', 'imprint', 'due_back', 'status')
  fieldsets = (
                (None, 
                  {'fields': ('book', 'imprint', 'id')}
                ),
                (
                  'Availability', {'fields': ('status', 'due_back')}
                ),
              )
