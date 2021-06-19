from django import template

# Custom tag to make alerts

register = template.Library()

@register.inclusion_tag('alerts.html')
def alert(message_obj):
  return {'alert': message_obj}