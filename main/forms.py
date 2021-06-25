from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from .models import Profile

class NewPost(forms.Form):
  text = forms.CharField(widget=TinyMCE())


class RegisterForm(UserCreationForm):
  email = forms.EmailField(max_length=240)

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

class UpdateProfileBio(forms.Form):
  bio = forms.CharField(max_length=200, required=False, widget=forms.Textarea)


class UpdateProfileAvatar(forms.Form):
  avatar_img = forms.ImageField()