from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_enumfield import enum


class Roles(enum.Enum):
    ADMIN = 0
    USER = 1


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # role = enum.EnumField(Roles)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]