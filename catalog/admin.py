from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

class BooksInline(admin.TabularInline):
  """docstring for BooksInstanceInline"""
  model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
  inlines = [BooksInline]

class BooksInstanceInline(admin.TabularInline):
  """docstring for BooksInstanceInline"""
  model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'display_genre')
  inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ('book', 'imprint','borrower', 'due_back', 'status', 'id')
  list_filter = ('status', 'due_back')

  fieldsets = (
    (None, {
      'fields': ('book', 'imprint', 'id')
    }),
    ('Availability', {
      'fields': ('status', 'due_back', 'borrower')
    }),
  )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
  """docstring for Genre"""
  pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
  """docstring for Genre"""
  pass
