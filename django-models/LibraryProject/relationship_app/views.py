from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from .models import Library
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

# Function-based View to list all books
def list_books(request):
    books = Book.objects.all()  
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  
    context_object_name = 'library'



class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
          
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')  
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})



def is_admin(user):
    return user.userprofile.role == 'Admin'


def is_librarian(user):
    return user.userprofile.role == 'Librarian'


def is_member(user):
    return user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Welcome Admin!")


@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Welcome Librarian!")


@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Welcome Member!")


