from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


# عرض تسجيل الدخول
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'auth/login.html', {'error': 'المستخدم أو كلمة المرور غير صحيحة'})
    return render(request, 'auth/login.html')


# تسجيل الخروج
def user_logout(request):
    logout(request)
    return redirect('login')


# عرض نموذج التسجيل
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


# عرض وتحرير الملف الشخصي
@login_required
def user_profile(request):
    if request.method == 'POST':
        # معالجة التحديثات
        new_email = request.POST.get('email')
        request.user.email = new_email
        request.user.save()
        return redirect('profile')
    return render(request, 'auth/profile.html', {'user': request.user})