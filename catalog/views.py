from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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

