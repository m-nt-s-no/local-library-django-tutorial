from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_books_w_fire = Book.objects.filter(title__icontains = 'fire').count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_books_w_fire': num_books_w_fire,
        'num_instances': num_instances,
        'num_genres': num_genres,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def book_list(request):

    #Titles and authors of available books
    available = BookInstance.objects.filter(status__exact='a')
    available_books = [(instance.book.title, instance.book.author) for instance in available]

    #Remove duplicate titles and sort by title ascending
    available_books = list(set(available_books))
    available_books.sort(key = lambda x: x[0])

    context = {"available_books": available_books}

    return render(request, 'book_list.html', context = context)