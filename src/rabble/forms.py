from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'anon']
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        'anon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
    labels = {
        'title': 'Title',
        'body': 'Body',
        'anon': 'Anonymous'
    }