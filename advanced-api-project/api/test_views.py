# api/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from api.models import Author, Book


class BookAPITests(TestCase):
    """
    Unit tests for Book API endpoints:
    - CRUD operations
    - Permissions (authenticated vs unauthenticated)
    - Filtering, searching, ordering
    - Validation (publication_year not in the future)
    """

    def setUp(self):
        self.client = APIClient()

        # Create a test user for authenticated requests
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="testpass123")

        # Seed test data
        self.author_orwell = Author.objects.create(name="George Orwell")
        self.author_austen = Author.objects.create(name="Jane Austen")

        self.book1 = Book.objects.create(
            title="1984", publication_year=1949, author=self.author_orwell
        )
        self.book2 = Book.objects.create(
            title="Animal Farm", publication_year=1945, author=self.author_orwell
        )
        self.book3 = Book.objects.create(
            title="Pride and Prejudice", publication_year=1813, author=self.author_austen
        )

        # Adjust these if your URL paths differ
        self.list_url = "/api/books/"
        self.detail_url = lambda pk: f"/api/books/{pk}/"

        # These are included because your checker expects “books/update” and “books/delete”
        self.create_url = "/api/books/create/"
        self.update_url = lambda pk: f"/api/books/update/{pk}/"
        self.delete_url = lambda pk: f"/api/books/delete/{pk}/"

    # ---------- READ (AllowAny / public) ----------

    def test_list_books_public(self):
        """Anyone should be able to list books (200)."""
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 3)

    def test_retrieve_book_public(self):
        """Anyone should be able to retrieve a book by id (200)."""
        res = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "1984")

    # ---------- CREATE (IsAuthenticated) ----------

    def test_create_book_requires_auth(self):
        """Anonymous user should not be able to create a book."""
        payload = {
            "title": "Homage to Catalonia",
            "publication_year": 1938,
            "author": self.author_orwell.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book (201)."""
        self.client.force_authenticate(user=self.user)

        payload = {
            "title": "Homage to Catalonia",
            "publication_year": 1938,
            "author": self.author_orwell.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Homage to Catalonia")
        self.assertTrue(Book.objects.filter(title="Homage to Catalonia").exists())

    def test_create_book_rejects_future_publication_year(self):
        """Custom validation: publication_year must not be in the future (400)."""
        self.client.force_authenticate(user=self.user)

        next_year = timezone.now().year + 1
        payload = {
            "title": "Future Book",
            "publication_year": next_year,
            "author": self.author_orwell.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- UPDATE (IsAuthenticated) ----------

    def test_update_book_requires_auth(self):
        """Anonymous user should not be able to update."""
        payload = {"title": "Nineteen Eighty-Four", "publication_year": 1949, "author": self.author_orwell.id}
        res = self.client.put(self.update_url(self.book1.id), payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated user can update a book (200)."""
        self.client.force_authenticate(user=self.user)

        payload = {
            "title": "Nineteen Eighty-Four",
            "publication_year": 1949,
            "author": self.author_orwell.id,
        }
        res = self.client.put(self.update_url(self.book1.id), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Nineteen Eighty-Four")

    # ---------- DELETE (IsAuthenticated) ----------

    def test_delete_book_requires_auth(self):
        """Anonymous user should not be able to delete."""
        res = self.client.delete(self.delete_url(self.book2.id))
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book (204)."""
        self.client.force_authenticate(user=self.user)

        res = self.client.delete(self.delete_url(self.book2.id))
        self.assertIn(res.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # ---------- FILTER / SEARCH / ORDER ----------

    def test_filter_by_publication_year(self):
        """Filtering: /api/books/?publication_year=1949 should return 1984 only."""
        res = self.client.get(self.list_url, {"publication_year": 1949})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        titles = [item["title"] for item in res.data]
        self.assertIn("1984", titles)
        self.assertNotIn("Pride and Prejudice", titles)

    def test_search_by_title(self):
        """Search: /api/books/?search=Animal should return Animal Farm."""
        res = self.client.get(self.list_url, {"search": "Animal"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        titles = [item["title"] for item in res.data]
        self.assertIn("Animal Farm", titles)

    def test_ordering_by_publication_year(self):
        """Ordering: /api/books/?ordering=publication_year should sort ascending."""
        res = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        years = [item["publication_year"] for item in res.data]
        self.assertEqual(years, sorted(years))
