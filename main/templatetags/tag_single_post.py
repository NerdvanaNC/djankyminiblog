from django import template

# Custom tag to make alerts

register = template.Library()

@register.inclusion_tag('single_post.html')
def single_post(post_obj, user_obj):
  return {'post': post_obj, 'user': user_obj}