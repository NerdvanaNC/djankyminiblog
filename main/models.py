from django.db import models
from tinymce import models as tinymodels
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post", null=True)
  text = tinymodels.HTMLField(max_length=5000)
  likes = models.IntegerField()
  createdAt = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.text