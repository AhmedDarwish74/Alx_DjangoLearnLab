from django.contrib import admin
from .models import Book
from .models import CustomUser

class BookAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'author', 'publication_year')

   
    search_fields = ('title', 'author')

   
    list_filter = ('publication_year',)



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
