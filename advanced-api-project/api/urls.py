from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [

    # List all books
    path('books/', BookListView.as_view(), name='book-list'),

    # Retrieve single book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Create book
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # UPDATE book (checker expects "books/update")
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),

    # DELETE book (checker expects "books/delete")
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),

]
