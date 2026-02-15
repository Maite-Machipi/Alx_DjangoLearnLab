from django.db import models


class Author(models.Model):
    """
    Author model:
    Stores an author's name.

    Relationship:
    One Author can have many Books (one-to-many).
    Django automatically creates a reverse relationship:
    author.book_set.all() unless related_name is set.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    Stores book details and links each Book to an Author.

    Fields:
    - title: book title
    - publication_year: year book was published
    - author: ForeignKey to Author (many books can share one author)
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"  # allows: author.books.all()
    )

    def __str__(self):
        return self.title
