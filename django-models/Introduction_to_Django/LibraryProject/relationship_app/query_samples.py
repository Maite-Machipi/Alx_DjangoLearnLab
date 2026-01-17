# query_samples.py
# Sample ORM queries demonstrating relationships

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """Query all books by a specific author."""
    return Book.objects.filter(author__name=author_name)


def list_books_in_library(library_name):
    """List all books in a library."""
    library = Library.objects.get(name=library_name)
    return library.books.all()


def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)
