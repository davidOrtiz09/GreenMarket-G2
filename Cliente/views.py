# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class Index(View):
    def get(self, request):
        return render(request, 'Cliente/index.html', {})


class UpdateShoppingCart(View):
    def post(self, request):
        # Se añade un nuevo item al carrito de compras (almacenado en la sesión) y se le notifica al usuario
        # Se retorna a la página desde el que se añadió el producto al carrito
        product_id = int(request.POST.get('product_id', '0'))
        quantity = int(request.POST.get('quantity', '0'))

        if product_id > 0 and quantity != 0:
            cart = request.session.get('cart', None)
            if not cart:
                cart = {
                    'items': [{
                        'product_id': product_id,
                        'quantity': quantity
                    }]
                }
            else:
                items = cart.get('items', [])
                exists = False
                i = 0
                while not exists and i < len(items):
                    item = items[i]
                    if item['product_id'] == product_id:
                        item['quantity'] += quantity
                        exists = True
                    i += 1
                if not exists:
                    items.append({
                        'product_id': product_id,
                        'quantity': quantity
                    })
                cart['items'] = items

            request.session['cart'] = cart
            messages.add_message(request, messages.SUCCESS, 'El producto se agregó al carrito satisfactoriamente')
        return redirect(request.META.get('HTTP_REFERER', '/'))
