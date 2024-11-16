from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView



def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
def home(request):
    return render(request, 'relationship_app/home.html')
# Custom registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})