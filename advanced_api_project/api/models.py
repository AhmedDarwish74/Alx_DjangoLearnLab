from django.db import models

# نموذج المؤلف
# يُمثل المؤلفين الذين يمكنهم تأليف عدة كتب.
class Author(models.Model):
    name = models.CharField(max_length=255)  
# نموذج الكتاب
# يُمثل الكتب المرتبطة بالمؤلفين عبر العلاقة ForeignKey.
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)  
    publication_year = models.PositiveIntegerField()  
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  

    def __str__(self):
        return self.title
