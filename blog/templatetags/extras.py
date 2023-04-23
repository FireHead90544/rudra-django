from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    return [val.strip() for val in value.split(arg)]

@register.filter(name='age')
def age(value):
    val = value.split(",")[0]
    if val == "now":
        return val
    return val + " ago" if not val.endswith("ago") else val

@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)

@register.filter(name='replace')
def replace(value, arg):
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)