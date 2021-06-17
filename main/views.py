from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewPost, RegisterForm
from .models import Post
import bleach
import datetime
from django.utils import timezone

bleach_allowed_tags = ['pre', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'span']
bleach_allowed_attrs = { '*': ['style'], 'a': ['href', 'title', '_target'] }
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
          u = response.user
          now = timezone.now()
          if (now - u.profile.last_post).total_seconds() > 86400 or u.id == 2:
            # We only allows posts once every 24 hours
            # But this limit doesn't apply to me, as I'm the admin
            post_text = bleach.clean(form.cleaned_data['text'], tags=bleach_allowed_tags, attributes=bleach_allowed_attrs, styles=bleach_allowed_styles)
            p = Post(text = post_text, likes = 0, author = u)
            p.save()
            u.profile.last_post = datetime.datetime.now()
            u.save()
            return HttpResponseRedirect('/?msg=Done! Your story is out in the world.') # If everything's cool; return back to the homepage with a blank form.
          else:
            return HttpResponseRedirect('/?msg=You need to wait 24 hours before posting again.')
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
    u = response.user
    if p:
      p = p[0]
      post_already_liked = u.profile.liked_posts.filter(id=p.id)
      if post_already_liked:
        return JsonResponse({'result': 'Already liked.'})
      else:
        likes = p.post_like()
        p.save()
        u.profile.liked_posts.add(p)
        return JsonResponse({'result': likes})

    else:
      return JsonResponse({'result': 'Not found.'})
  else:
    return JsonResponse({'result': "Invalid arguments."})

def ajax_unlike(response):
  if response.GET.get('id'):
    p = Post.objects.filter(id=(response.GET.get('id')))
    u = response.user
    if p:
      p = p[0]
      post_already_liked = u.profile.liked_posts.filter(id=p.id)
      if post_already_liked:
        likes = p.post_unlike()
        p.save()
        u.profile.liked_posts.remove(p)
        return JsonResponse({'result': likes})
      else:
        return JsonResponse({'result': 'Not liked.'})

    else:
      return JsonResponse({'result': 'Not found.'})
  else:
    return JsonResponse({'result': "Invalid arguments."})


def user_profile(response, username):
  requested_user = User.objects.filter(username=username)
  view_path = response.path
  if requested_user:
    requested_user = requested_user[0]
    authored_posts = Post.objects.filter(author=requested_user)
    liked_posts = requested_user.profile.liked_posts.all()

    if view_path.find('liked') >= 0:
      if liked_posts:
        current_page = response.GET.get('page', 1)
        paginator_obj = Paginator(liked_posts, 5)
        try:
          page_obj = paginator_obj.page(current_page)
        except PageNotAnInteger:
          page_obj = paginator_obj.page(1)
        except EmptyPage:
          page_obj = paginator_obj.page(paginator_obj.num_pages)
      else:
        page_obj = None

      page_active = 'liked'
    else:
      if authored_posts:
        current_page = response.GET.get('page', 1)
        paginator_obj = Paginator(authored_posts, 5)
        try:
          page_obj = paginator_obj.page(current_page)
        except PageNotAnInteger:
          page_obj = paginator_obj.page(1)
        except EmptyPage:
          page_obj = paginator_obj.page(paginator_obj.num_pages)
      else:
        page_obj = None

      page_active = 'authored'

    response_obj = {'requested_user': requested_user, 'page_obj': page_obj, 'active': page_active}
    return render(response, 'main/profile.html', response_obj)
  else:
    return HttpResponseRedirect('/?msg=User not found; did you get the username right?')


def about(response):
  return render(response, 'main/about.html', {'navactive': 'about'})