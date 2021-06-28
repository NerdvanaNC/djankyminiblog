from django.db import models
from tinymce import models as tinymodels
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Model Helpers
def now_minus_25hours():
  return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=25)


# Create your models here.
class Post(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post", null=True)
  text = tinymodels.HTMLField()
  likes = models.IntegerField()
  createdAt = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-createdAt']

  def __str__(self):
    return self.text

  def post_like(self):
    self.likes += 1
    return self.likes

  def post_unlike(self):
    self.likes -= 1
    return self.likes


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  createdAt = models.DateTimeField(auto_now_add=True)
  last_post = models.DateTimeField(default=now_minus_25hours)
  liked_posts = models.ManyToManyField(Post)
  bio = models.CharField(max_length=200, default='Very creative with their posts, but they haven\'t added a bio yet.')
  avatar = models.CharField(max_length=600, default='https://picsum.photos/512/')
  # more profile details will go here
  # to extend the base User model provided
  # by Django.

# When User is saved, but as a creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

# When User is saved, but as an update
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()