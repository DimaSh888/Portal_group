from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=['Student', 'Teacher', 'Administrator']
        ),
        empty_label=None,
        label='Role'
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