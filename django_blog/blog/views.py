from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib.auth import update_session_auth_hash


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login')  
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})



@login_required
def profile(request):
    """Showing users data"""
    if request.method == 'POST':
     
        request.user.email = request.POST.get('email')
        request.user.save()
        return redirect('profile')
    
    return render(request, 'auth/profile.html', {'user': request.user})