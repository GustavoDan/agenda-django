from django import template

register = template.Library()


@register.filter(name="split")
def split(value, separator):
    return value.split(separator)


@register.simple_tag
def replace(value, old, new):
    return value.replace(old, new)
