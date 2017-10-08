from django import template

register = template.Library()


@register.filter(name='to_cop')
def to_cop(number):
    try:
        return format(number, ',.0f')
    except Exception as e:
        return number


@register.filter(name='multiply_cop')
def multiply_cop(value, arg):
    try:
        return to_cop(float(value * arg))
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter(name='count_cart_products')
def count_cart_products(request):
    cart = request.session.get('cart', None)
    response = 0
    if cart:
        items = cart.get('items', [])
        for item in items:
            response += item['quantity']
    return response
