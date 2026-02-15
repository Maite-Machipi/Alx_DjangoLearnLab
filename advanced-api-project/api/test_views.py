# api/test_views.py

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    APITestCase is required by Django REST Framework.
    It provides built-in support for API testing.
    """

    def setUp(self):
        self.client = APIClient()

        # Create test user
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            password="testpass123"
        )

        # Create authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Jane Austen")

        # Create books
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1
        )

        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1
        )

        # URLs
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book1.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/update/{self.book1.id}/"
        self.delete_url = f"/api/books/delete/{self.book1.id}/"

    # -------------------------
    # READ TESTS
    # -------------------------

    def test_list_books(self):
        """Test retrieving list of books"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Test retrieving single book"""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")

    # -------------------------
    # CREATE TESTS
    # -------------------------

    def test_create_book_authenticated(self):
        """Test authenticated user can create book"""

        self.client.force_authenticate(user=self.user)

        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_create_book_unauthenticated(self):
        """Test unauthenticated user cannot create book"""

        data = {
            "title": "Unauthorized Book",
            "publication_year": 2020,
            "author": self.author1.id
        }

        response = self.client.post(self.create_url, data)

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

    # -------------------------
    # UPDATE TESTS
    # -------------------------

    def test_update_book_authenticated(self):

        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Updated Title",
            "publication_year": 1949,
            "author": self.author1.id
        }

        response = self.client.put(self.update_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()

        self.assertEqual(self.book1.title, "Updated Title")

    # -------------------------
    # DELETE TESTS
    # -------------------------

    def test_delete_book_authenticated(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.delete_url)

        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
        )

        self.assertFalse(
            Book.objects.filter(id=self.book1.id).exists()
        )

    # -------------------------
    # VALIDATION TEST
    # -------------------------

    def test_publication_year_validation(self):

        self.client.force_authenticate(user=self.user)

        future_year = timezone.now().year + 5

        data = {
            "title": "Future Book",
            "publication_year": future_year,
            "author": self.author1.id
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
