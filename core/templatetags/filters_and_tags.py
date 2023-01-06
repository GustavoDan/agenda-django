from django import template

register = template.Library()


@register.filter(name="split")
def split(value, separator):
    return value.split(separator)


@register.filter(name="get_field_label")
def get_field_label(form, field):
    return form.fields[field].label


@register.simple_tag
def replace(value, old, new):
    return value.replace(old, new)
