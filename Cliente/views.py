# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages


class Index(View):
    def get(self, request):
        return render(request, 'Cliente/index.html', {})


class Checkout(View):
    def get(self, request):
        cart = request.session.get('cart', None)
        items = []
        if cart:
            items = cart.get('items', [])

        if not cart or len(items) == 0:
            messages.add_message(request, messages.WARNING, 'No tienes productos en tu carrito de compras')
            return redirect(reverse('cliente:index'))
        else:
            return render(request, 'Cliente/checkout/checkout.html', {})


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


class DeleteProductFromShoppingCart(View):
    def post(self, request):
        cart = request.session.get('cart', None)
        product_id = int(request.POST.get('product-id', '-1'))
        if cart:
            items = cart.get('items', [])
            index = -1
            i = 0
            while i < len(items) and index == -1:
                item = items[i]
                if item['product_id'] == product_id:
                    index = i
                i += 1

            if index >= 0:
                items.remove(items[index])
                cart['items'] = items
                request.session['cart'] = cart
        return redirect(reverse('cliente:checkout'))
