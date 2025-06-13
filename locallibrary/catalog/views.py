from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
import datetime

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

@login_required
@permission_required('catalog.can_mark_returned')
def all_borrowed(request):
    """view of all borrowed books, for librarians only."""
    all_borrowed_books = BookInstance.objects.filter(status = 'o')

    context = {"all_borrowed_books": all_borrowed_books}

    return render(request, 'all_borrowed.html', context = context)

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
    
class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('books')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)