from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import EmailField, CharField
# from captcha.fields import ReCaptchaField

class UserCreationForm(UserCreationForm):
    email = EmailField(label=("Email address"), required=True,
        help_text=("Required."))


    class Meta:
        model = User
        fields = ("username", "email", "first_name","last_name","password1", "password2")

# class FormWithCaptcha(forms.Form):
#     captcha = ReCaptchaField(
#     public_key='6Lf35GIUAAAAABPXR9iv4B3s-cM3Kvv55cEQwhsD',
#     private_key='6Lf35GIUAAAAAFg4uWQAkyQtBLhIVVP5ZvXJnp9b',
#     )
