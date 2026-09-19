from django import forms
from .models import Category, Post, Topic


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")

        labels = {
            "name": "Category name",
            "description": "Category description",
        }

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Short description of this category...",
                }
            ),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "image")
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your comment...",
                }
            ),
        }
        labels = {
            "content": "Your comment",
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("category", "title")
        labels = {
            "category": "Category",
            "title": "Topic name",
        }