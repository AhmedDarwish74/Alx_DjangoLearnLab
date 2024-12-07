from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_blog.blog.models import Post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  #add email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']