# app_orders/templatetags/cart_filters.py

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica dos valores"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def intcomma(value):
    """Formatea números con separadores de miles"""
    try:
        value = int(float(value))
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value

@register.filter
def range_list(value):
    """Genera un rango de 1 hasta el valor dado"""
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(1, 2)