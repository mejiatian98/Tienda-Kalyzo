from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return (1 - (value / arg)) * 100
    except:
        return 0
