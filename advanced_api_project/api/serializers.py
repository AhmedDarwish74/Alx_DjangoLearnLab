from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes the Book model fields.
    Ensures data validation for publication_year to disallow future years.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Ensure the `publication_year` is not set in the future.
        """
        from datetime import datetime
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model fields and nests a dynamic list of related books using BookSerializer.
    """
    
    # Nesting BookSerializer here to dynamically serialize related books
    books = BookSerializer(source='book_set', many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']