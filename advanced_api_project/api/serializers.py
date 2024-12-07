from rest_framework import serializers
from .models import Author, Book

# السلسلة الخاصة بالكتب
# تُسلسِل نموذج الكتاب مع التحقق من صحة السنة. 
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    
    def validate_publication_year(self, value):
        from datetime import datetime
        if value > datetime.now().year:
            raise serializers.ValidationError("يجب أن تكون سنة النشر أقل من أو تساوي السنة الحالية.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
