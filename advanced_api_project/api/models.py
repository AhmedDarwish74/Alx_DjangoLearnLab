from django.db import models

class Author(models.Model):
    """
    Model representing an author.
    - `name`: Represents the name of the author.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a book.
    - `title`: Represents the title of the book.
    - `publication_year`: The year the book was published.
    - `author`: ForeignKey to link each book to its author (establishing one-to-many relationship).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
