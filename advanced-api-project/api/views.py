from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /books/
    Public: List all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/
    Public: Retrieve one book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Authenticated only: Create a new book.
    Uses BookSerializer validation (e.g., publication_year not in future).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<pk>/update/
    Authenticated only: Update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/delete/
    Authenticated only: Delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
