from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NewPost
from .models import Post

# Create your views here.
def main(response):
  all_posts = Post.objects.all()
  if response.method == 'POST':
    form = NewPost(response.POST)
    if form.is_valid():
      post_text = form.cleaned_data['text']
      p = Post(text = post_text, likes = 0)
      p.save()
      return HttpResponseRedirect('/') # If everything's cool; return back to the homepage with a blank form.
  else:
    form = NewPost()
    
  return render(response, 'main/homepage.html', {'form': form, 'all_posts': all_posts})

def about(response):
  return render(response, 'main/about.html', {})