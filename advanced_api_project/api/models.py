from django.db import models

class Author(models.Model):
    """
    Represents an author of books.
    Fields:
    - name: The name of the author.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book.
    Fields:
    - title: The title of the book.
    - publication_year: The year the book was published.
    - author: A ForeignKey linking the book to an author.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
