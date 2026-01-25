from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookSearchForm
from .forms import ExampleForm

def form_example(request):
    form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})



@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()

    # Safe input handling (prevents SQL injection by using Django ORM)
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})
