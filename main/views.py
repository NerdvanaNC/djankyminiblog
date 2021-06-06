from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import NewPost, RegisterForm
from .models import Post
import bleach

bleach_allowed_tags = ['pre', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul']
bleach_allowed_styles = ['color', 'font-family', 'font-size', 'text-decoration', 'text-align']


# Create your views here.
def main(response):
  all_posts = Post.objects.all()

  if response.user.is_authenticated:
    # User logged in
    if response.method == 'POST':
      if 'post' in response.POST:
        form = NewPost(response.POST)
        if form.is_valid():
          post_text = bleach.clean(form.cleaned_data['text'], tags=bleach_allowed_tags, styles=bleach_allowed_styles)
          u = response.user
          p = Post(text = post_text, likes = 0, user = u)
          p.save()
          return HttpResponseRedirect('/') # If everything's cool; return back to the homepage with a blank form.
    else:
      form = NewPost()
  else:
    if response.method == 'POST':
      if 'login' in response.POST:
        form = AuthenticationForm(response.POST)
        username = response.POST.get('username')
        password = response.POST.get('password')
        user = authenticate(response, username=username, password=password)
        if user is not None:
          login(response, user)
          return HttpResponseRedirect('/?msg=Welcome back!')
        else:
          return HttpResponseRedirect('/?err=Invalid Credentials. Please try again.')
    else:
      form = AuthenticationForm()

  return render(response, 'main/homepage.html', {'form': form, 'all_posts': all_posts})


def custom_register(response):
  if response.method == 'POST':
    form = RegisterForm(response.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(response, username=username, password=password)
      if user is not None:
        login(response, user)
        return HttpResponseRedirect('/?msg=Welcome!')
  else:
    form = RegisterForm()

  return render(response, 'main/register.html', {'form': form})


def custom_logout(response):
  logout(response)
  return HttpResponseRedirect('/?msg=You\'ve logged out.')


def about(response):
  return render(response, 'main/about.html', {})