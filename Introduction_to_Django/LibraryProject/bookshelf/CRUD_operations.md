# CRUD Operations for Book Model

## 1. Create a Book (إنشاء الكتاب)

**Command**:
```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
