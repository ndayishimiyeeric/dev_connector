from django import template

register = template.Library()


@register.filter
def hasattr(obj, attr):
    return hasattr(obj, attr)
