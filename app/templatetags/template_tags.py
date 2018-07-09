from django import template
from django.conf import settings

register = template.Library()

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.assignment_tag
def query(qs, **kwargs):
    return qs.filter(**kwargs)

@register.filter
def convertblank(val):
    if(val == 0):
        return ''
    else:
        return val

