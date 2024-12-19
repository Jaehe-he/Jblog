from django import forms
from .models import Post, Category, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category']  # 추가할 필드

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']