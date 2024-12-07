from tokenize import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_blog.blog.models import Post
from .models import Post
from taggit.forms import TagWidget


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  #add email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # أضف حقول النموذج المطلوبة
        widgets = {
            'tags': TagWidget(),  # تأكد من تضمين TagWidget في الwidgets
        }