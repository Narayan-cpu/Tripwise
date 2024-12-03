from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'story']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
