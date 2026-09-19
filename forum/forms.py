from django import forms
from .models import Category, Post, Topic


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {
            "name": "Category name",
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)
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