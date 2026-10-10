from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Administrator', 'Administrator'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Role',
        widget=forms.Select()
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'role',
        )


class RegisterForm2(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First name',
            'last_name': 'Last name',
        }


class AdminUserForm(forms.ModelForm):

    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Administrator', 'Administrator'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Role'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First name',
            'last_name': 'Last name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.is_superuser:
            self.fields['role'].initial = 'Administrator'
        elif self.instance.groups.filter(name='Teacher').exists():
            self.fields['role'].initial = 'Teacher'
        elif self.instance.groups.filter(name='Student').exists():
            self.fields['role'].initial = 'Student'
        else:
            self.fields['role'].initial = 'Student'


from .models import GalleryImage, PortfolioWork


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ("title", "description", "image")
        labels = {
            "title": "Title",
            "description": "Description",
            "image": "Image",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class PortfolioWorkForm(forms.ModelForm):
    class Meta:
        model = PortfolioWork
        fields = ("title", "description", "image", "project_url")
        labels = {
            "title": "Title",
            "description": "Description",
            "image": "Preview image (optional)",
            "project_url": "Project link (optional)",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
