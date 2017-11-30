from django import template
from json import dumps
register = template.Library()


# Dado un numero, lo retorna en formato moneda para que sea mas legible
@register.filter(name='to_cop')
def to_cop(number):
    try:
        return format(number, ',.0f')
    except Exception as e:
        return number


@register.filter(name='dumps_filter')
def dumps_filter(d):
    try:
        return dumps(d)
    except Exception as e:
        return d

# Funcionalidad para multiplicar en templates y retornar el resultado en formato moneda
@register.filter(name='multiply_cop')
def multiply_cop(value, arg):
    try:
        return to_cop(float(value * arg))
    except (ValueError, ZeroDivisionError):
        return 0


# Funcionalidad para multiplicar en templates y retornar el resultado
@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value * arg)
    except (ValueError, ZeroDivisionError):
        return 0
