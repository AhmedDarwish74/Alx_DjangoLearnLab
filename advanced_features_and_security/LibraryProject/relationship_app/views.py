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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .forms import BookForm


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


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')



@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        
        title = request.POST.get("title")
        author = request.POST.get("author")
        publication_date = request.POST.get("publication_date")
        Book.objects.create(title=title, author=author, publication_date=publication_date)
        return redirect('book_list')
    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.publication_date = request.POST.get("publication_date")
        book.save()
        return redirect('book_list')
    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)  
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()  
            return redirect('list_books')  
    else:
        form = BookForm(instance=book)  
    return render(request, 'relationship_app/edit_book.html', {'form': form})