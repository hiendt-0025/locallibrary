from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Language
from django.views import generic

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

