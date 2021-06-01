from django import forms
from django.contrib.auth.forms import AuthenticationForm

class NewPost(forms.Form):
  text = forms.CharField(label="", max_length=240, widget=(forms.TextInput(
    attrs={"class": "new-post form-control", "placeholder": "What's on your mind?"})))

class LoginForm(AuthenticationForm):
  username = forms.CharField(label="", max_length=240, widget=(forms.TextInput(
    attrs={"class": "username form-control", "placeholder": "Username"})))
  password = forms.CharField(label="", max_length=240, widget=(forms.PasswordInput(
    attrs={"class": "password form-control", "placeholder": "Password"})))