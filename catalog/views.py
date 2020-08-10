from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Language

def index(request):
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()

  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  num_authors = Author.objects.count()

  num_genre = Genre.objects.count()

  num_books_available = Book.objects.filter(title__contains='Nhung').count()

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genre': num_genre,
    'num_books_available': num_books_available,
  }

  return render(request, 'index.html', context = context)
