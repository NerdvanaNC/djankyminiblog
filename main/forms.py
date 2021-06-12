from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class NewPost(forms.Form):
  text = forms.CharField(widget=TinyMCE())

class RegisterForm(UserCreationForm):
  email = forms.EmailField(max_length=240)

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')