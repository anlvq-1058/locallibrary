import datetime
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookModelForm
from catalog.models import Book, Author, BookInstance, Genre

@login_required
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

class BookDetailView(LoginRequiredMixin, generic.DetailView):
  model = Book

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  model = BookInstance
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['bookinstance_list'] = BookInstance.objects.filter(borrower = self.request.user)
    return context
  def get_template_names(self):
    return ['catalog/bookinstance_list_borrowed_user.html']

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
  """View function for renewing a specific BookInstance by librarian."""
  book_instance = get_object_or_404(BookInstance, pk=pk)
  if request.method == 'POST':
    form = RenewBookModelForm(request.POST)
    if form.is_valid():
      book_instance.due_back = form.cleaned_data['due_back']
      book_instance.save()
      return HttpResponseRedirect(reverse('my-borrowed') )
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
  context = {
              'form': form,
              'book_instance': book_instance,
            }
  return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
  initial = {'date_of_death': '11/11/2023'}
  permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
  model = Author
  # Not recommended (potential security issue if more fields added)
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
  permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
  model = Author
  success_url = reverse_lazy('authors')
  permission_required = 'catalog.delete_author'

  def form_valid(self, form):
    try:
      self.object.delete()
      return HttpResponseRedirect(self.success_url)
    except Exception as e:
      return HttpResponseRedirect(
          reverse("author-delete", kwargs={"pk": self.object.pk})
      )
class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()

class AuthorDetailView(generic.DetailView):
  model = Author

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context
