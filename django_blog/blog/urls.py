from django.urls import path
from .views import register, profile
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/auth/login/'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]