from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class NewPost(forms.Form):
  text = forms.CharField()

class RegisterForm(UserCreationForm):
  email = forms.EmailField(max_length=240)

  class Meta:
    model = User
    fields = ('email', 'password1', 'password2')