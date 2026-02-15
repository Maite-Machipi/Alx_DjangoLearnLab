# api/test_views.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):

        self.client = APIClient()

        # Create user
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            password="testpass123"
        )

        # LOGIN USER (Required by checker)
        self.client.login(username="tester", password="testpass123")

        # Create author
        self.author = Author.objects.create(name="George Orwell")

        # Create book
        self.book = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )

        # URLs
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/update/{self.book.id}/"
        self.delete_url = f"/api/books/delete/{self.book.id}/"


    # -------------------------
    # TEST LIST
    # -------------------------

    def test_list_books(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # -------------------------
    # TEST DETAIL
    # -------------------------

    def test_retrieve_book(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")


    # -------------------------
    # TEST CREATE
    # -------------------------

    def test_create_book(self):

        data = {
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # -------------------------
    # TEST UPDATE
    # -------------------------

    def test_update_book(self):

        data = {
            "title": "Updated Title",
            "publication_year": 1949,
            "author": self.author.id
        }

        response = self.client.put(self.update_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # -------------------------
    # TEST DELETE
    # -------------------------

    def test_delete_book(self):

        response = self.client.delete(self.delete_url)

        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
        )


    # -------------------------
    # VALIDATION TEST
    # -------------------------

    def test_publication_year_not_future(self):

        future_year = timezone.now().year + 1

        data = {
            "title": "Future Book",
            "publication_year": future_year,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
