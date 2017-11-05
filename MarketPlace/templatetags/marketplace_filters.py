from django import template

register = template.Library()


# Dado un numero, lo retorna en formato moneda para que sea mas legible
@register.filter(name='to_cop')
def to_cop(number):
    try:
        return format(number, ',.0f')
    except Exception as e:
        return number


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
        return 0  # Cuenta los items del carrito

# Cuenta los items del carrito
@register.filter(name='count_cart_products')
def count_cart_products(request):
    try:
        cart = request.session.get('cart', None)
        response = 0
        if cart:
            items = cart.get('items', [])
            for item in items:
                response += item['quantity']
        return response
    except:
        return 0
