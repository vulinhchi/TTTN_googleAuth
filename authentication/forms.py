from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import EmailField, CharField

class UserCreationForm(UserCreationForm):
    email = EmailField(label=("Email address"), required=True,
        help_text=("Required."))


    class Meta:
        model = User
        fields = ("username", "email", "first_name","last_name","password1", "password2")
