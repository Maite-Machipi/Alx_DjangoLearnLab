from datetime import date
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer:
    Serializes all fields of Book.

    Validation:
    Ensures publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer:
    Serializes the Author name and includes nested books.

    Relationship handling:
    Because Book.author uses related_name="books", we can serialize
    an author's books with `books` using BookSerializer(many=True).
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
