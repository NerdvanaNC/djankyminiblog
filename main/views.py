from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import NewPost, LoginForm
from .models import Post

# Create your views here.
def main(response):
  all_posts = Post.objects.all()
  if response.user.is_authenticated:
    # User logged in
    if response.method == 'POST':
      form = NewPost(response.POST)
      if form.is_valid():
        post_text = form.cleaned_data['text']
        p = Post(text = post_text, likes = 0)
        p.save()
        return HttpResponseRedirect('/') # If everything's cool; return back to the homepage with a blank form.
    else:
      form = NewPost()
  else:
    # User not logged in
    form = LoginForm()

  return render(response, 'main/homepage.html', {'form': form, 'all_posts': all_posts})

def custom_login(response):
  if response is not None:
    if response.method == 'POST':
      username = response.POST.get('username')
      password = response.POST.get('password')
      user = authenticate(response, username=username, password=password)
      if user is not None:
        login(response, user)

  return HttpResponseRedirect('/')

def custom_logout(response):
  logout(response)
  return HttpResponseRedirect('/')

def about(response):
  return render(response, 'main/about.html', {})