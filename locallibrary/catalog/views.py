from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Genres (count distinct genres)
    num_genres = Genre.objects.count()

    #Books that contain a particular word in the title
    word_in_title = Book.objects.filter(title__icontains='Harry').values_list('title', flat=True)
    title_string = ', '.join(word_in_title)
    word_in_title = f"Books containing 'Harry' in the title: {title_string}" if title_string else "No books found with 'Harry' in the title."

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'word_in_title': word_in_title
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic
class BookListView(generic.ListView):
    model = Book
    paginate_by = 3  # Show 10 books per page

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3  # Show 10 authors per page
class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        """Add in the books of the author."""
        context = super().get_context_data(**kwargs)
        context['author_books'] = Book.objects.filter(author=self.object)
        return context
