from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
  """View function for home page of site."""
  # Generate counts of some of the main objects
  num_books = Book.objects.count()
  num_instances = BookInstance.objects.count()
  num_visits = request.session.get('num_visits', 1)
  request.session['num_visits'] = num_visits + 1
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
  num_authors = Author.objects.count()
  context = {
             'num_books': num_books,
             'num_instances': num_instances,
             'num_instances_available': num_instances_available,
             'num_authors': num_authors,
             'num_visits': num_visits,
            }
  return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  queryset = Book.objects.all()
  paginate_by = 10

class BookDetailView(generic.DetailView):
  model = Book

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context
