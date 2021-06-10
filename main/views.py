from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewPost, RegisterForm
from .models import Post
import bleach

bleach_allowed_tags = ['pre', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul']
bleach_allowed_styles = ['color', 'font-family', 'font-size', 'text-decoration', 'text-align']


# Create your views here.
def main(response):
  # Infinite Scrolling Pagination
  # https://simpleisbetterthancomplex.com/tutorial/2017/03/13/how-to-create-infinite-scroll-with-django.html
  all_posts = Post.objects.all()
  current_page = response.GET.get('page', 1)
  paginator_obj = Paginator(all_posts, 5)

  if response.user.is_authenticated:
    try:
      page_obj = paginator_obj.page(current_page)
    except PageNotAnInteger:
      page_obj = paginator_obj.page(1)
    except EmptyPage:
      page_obj = paginator_obj.page(paginator_obj.num_pages)
  else:
    page_obj = all_posts[:5]


  # User Auth Flow
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
          return HttpResponseRedirect('/?msg=Hey, @{}.'.format(user.username))
        else:
          return HttpResponseRedirect('/?err=Invalid Credentials. Please try again.')
    else:
      form = AuthenticationForm()

  response_obj = {'form': form, 'page_obj': page_obj, 'navactive': 'home'}
  return render(response, 'main/homepage.html', response_obj)


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

def ajax_like(response):
  if response.GET.get('id'):
    p = Post.objects.filter(id=(response.GET.get('id')))
    if p:
      p = p[0]
      likes = p.post_like()
      p.save()
      return JsonResponse({'result': likes})
    else:
      return JsonResponse({'result': 'Not found.'})
  else:
    return JsonResponse({'result': "Invalid arguments."})


def about(response):
  return render(response, 'main/about.html', {'navactive': 'about'})