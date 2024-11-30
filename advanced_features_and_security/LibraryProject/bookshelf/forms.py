from django import forms
from .models import Book 

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="Title")
    author = forms.CharField(max_length=100, required=True, label="Author")
    publication_year = forms.IntegerField(min_value=1000, max_value=9999, required=True, label="Publication Year")
    
    
