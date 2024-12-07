from rest_framework import serializers
from .models import Author, Book


# Serializer for Book with custom validation for publication_year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation to ensure `publication_year` is not in the future
    def validate_publication_year(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for Author with nested serialization for related books
class AuthorSerializer(serializers.ModelSerializer):
    # Serialize all related books dynamically
    books = BookSerializer(many=True, read_only=True)  # Nested serialization for related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
