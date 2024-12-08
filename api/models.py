from django.db import models


# Author model to store author's name
class Author(models.Model):
    name = models.CharField(max_length=255) # Author's name

    def __str__(self):
        return self.name


# Book model with a foreign key relationship to Author
class Book(models.Model):
    title = models.CharField(max_length=255)# Book's title
    publication_year = models.IntegerField()# Year of publication
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")# Link to Author

    def __str__(self):
        return self.title
