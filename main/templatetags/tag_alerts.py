from django import template

# Custom tag to make alerts

register = template.Library()

@register.inclusion_tag('alerts.html')
def alert(dict_from_tag):
  if dict_from_tag.get('msg'):
    context = 'alert-info'
    text = dict_from_tag.get('msg')
  elif dict_from_tag.get('err'):
    context = 'alert-danger'
    text = dict_from_tag.get('err')
  else:
    context = "alert-info"
    text = ":)"

  return {'context': [context, text]}