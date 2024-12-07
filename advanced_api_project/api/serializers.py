from rest_framework import serializers
from api.models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes validation to ensure the publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        from datetime import datetime
        if value > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes nested serialization for related books.
    """
    books = BookSerializer(many=True, read_only=True)  # إنشاء علاقة تداخلية (nested relationship)

    class Meta:
        model = Author
        fields = ['name', 'books']
