import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.models import Book, Author, BookInstance, Genre, Language
from catalog.forms import RenewBookModelForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def index(request):
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()

  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  num_authors = Author.objects.count()

  num_genre = Genre.objects.count()

  num_books_available = Book.objects.filter(title__contains='Nhung').count()

  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits+1

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genre': num_genre,
    'num_books_available': num_books_available,
    'num_visits': num_visits,
  }

  return render(request, 'index.html', context = context)

class BookListView(generic.ListView):
  """docstring for BookListView"""
  model = Book
  paginate_by = 10

class BookDetailView(generic.DetailView):
  """docstring for BookDetailView"""
  model = Book

class AuthorListView(generic.ListView):
  """docstring for AuthorListView"""
  model = Author
  paginate_by = 10

class AuthorDetailView(generic.DetailView):
  """docstring for BookDetailView"""
  model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  """docstring for LoanedBooksByUserListView"""
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by =10

  def get_queryset(self):
    return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksByUserListView(LoginRequiredMixin,PermissionRequiredMixin, generic.ListView):
  """docstring for LoanedBooksByUserListView"""
  model = BookInstance
  permission_required = 'catalog.can_mark_returned'
  template_name = 'catalog/all_bookinstance_list_borrowed.html'
  paginate_by =10

  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk = pk)
  if request.method == 'POST':
    form = RenewBookModelForm(request.POST)
    if form.is_valid():
      book_instance.due_back = form.cleaned_data['due_back']
      book_instance.save()
      return HttpResponseRedirect(reverse('all-borrowed'))
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks =3)
    form = RenewBookModelForm(initial ={'due_back': proposed_renewal_date})

  context = {
    'form': form,
    'book_instance': book_instance,
  }
  return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
  """docstring for AuthorCreate"""
  model = Author
  fields = '__all__'
  initial={'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
  """docstring for AuthorUpdate"""
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
  """docstring for AuthorDelete"""
  model = Author
  success_url = reverse_lazy('authors')

class BookCreate(CreateView):
  """docstring for BookCreate"""
  model = Book
  fields = '__all__'
