from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

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

"""
def book_list(request):

    #Titles and authors of available books
    available = BookInstance.objects.filter(status__exact='a')
    available_books = [(instance.book.title, instance.book.author) for instance in available]

    #Remove duplicate titles and sort by title ascending
    available_books = list(set(available_books))
    available_books.sort(key = lambda x: x[0])

    context = {"available_books": available_books}

    return render(request, 'book_list.html', context = context)
"""

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'books'   # your own name for the list as a template variable

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["num_books"] = Book.objects.count()
        return context
    
class BookDetailView(generic.DetailView):
    model = Book

def authors(request):

    authors = Author.objects.all()
    context = {"authors": authors}

    return render(request, 'author_list.html', context = context)

def author_detail(request, pk):

    author = Author.objects.get(pk = pk)
    context = {"author": author}

    return render(request, 'author_detail.html', context = context)