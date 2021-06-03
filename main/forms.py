from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class NewPost(forms.Form):
  text = forms.CharField(label="", max_length=240, widget=(forms.TextInput(
    attrs={"class": "new-post form-control", "placeholder": "What's on your mind?"})))

class LoginForm(AuthenticationForm):
  username = forms.CharField(label="", max_length=240, widget=(forms.TextInput(
    attrs={"class": "username form-control", "placeholder": "Username"})))
  password = forms.CharField(label="", max_length=240, widget=(forms.PasswordInput(
    attrs={"class": "password form-control", "placeholder": "Password"})))

class RegisterForm(UserCreationForm):
  # email = forms.EmailField(label="Email", max_length=240, widget=(forms.TextInput(
  #   attrs={"class": "email form-control", "placeholder": "Email"})))
  # password1 = forms.CharField(label="Password", max_length=240, widget=(forms.PasswordInput(
  #   attrs={"class": "password1 form-control", "placeholder": "Password"})))
  # password2 = forms.CharField(label="Password (again)", max_length=240, widget=(forms.PasswordInput(
  #   attrs={"class": "password2 form-control", "placeholder": "Password (again)"})))

  class Meta:
    model = User
    fields = ('email', 'password1', 'password2')