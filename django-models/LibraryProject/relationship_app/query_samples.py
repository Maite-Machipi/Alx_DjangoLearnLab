from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    # Query all books by a specific author
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

def list_books_in_library(library_name):
    # List all books in a library
    library = Library.objects.get(name=library_name)
    return library.books.all()

def retrieve_librarian_for_library(library_name):
    # Retrieve the librarian for a library
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)
