from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookForm

@login_required
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

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'books'   # your own name for the list as a template variable

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["num_books"] = Book.objects.count()
        return context
    
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'authors'  

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

"""
def authors(request):

    authors = Author.objects.all()
    context = {"authors": authors}

    return render(request, 'author_list.html', context = context)

def author_detail(request, pk):

    author = Author.objects.get(pk = pk)
    context = {"author": author}

    return render(request, 'author_detail.html', context = context)
"""

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
def book_update(request, pk):
    book = Book.objects.get(pk = pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance = book)
        if form.is_valid():
            form.save()
            return redirect("book-detail", pk = book.pk)
    else:
        form = BookForm(instance = book)

    context = {"form": form}

    return render(request, "catalog/book_form.html", context=context)

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            created_book = form.save()
            return redirect("book-detail", pk = created_book.pk)
    else:
        form = BookForm()
    
    context = {"form": form}

    return render(request, "catalog/book_form.html", context=context)

def book_delete(request, pk):
    book = Book.objects.get(pk = pk)
    book.delete()
    return redirect("books")