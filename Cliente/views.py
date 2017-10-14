# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, render_to_response
from django.views import View
from django.contrib import messages
from Cliente.forms import ClientForm
from MarketPlace.models import Cliente, Catalogo_Producto, Categoria, Cooperativa
from django.contrib.auth.models import User


class Index(View):
    def get(self, request):
        cooperativas = Cooperativa.objects.all()
        producto_catalogo = Catalogo_Producto.objects\
            .filter(fk_catalogo__fk_cooperativa_id=cooperativas.first().id)\
            .order_by('fk_producto__nombre')
        categorias = Categoria.objects.all()
        return render(request, 'Cliente/index.html', {
            'productos_catalogo': producto_catalogo,
            'categorias': categorias,
            'cooperativas': cooperativas
        })

    def post(self, request):
        #Se listan los productos por Cooperativa y se ordenan segun filtro
        cooperativa_id = request.POST.get('cooperativa_id', '')
        ordenar_por = request.POST.get('ordenar', '')
        producto_catalogo = Catalogo_Producto.objects\
            .filter(fk_catalogo__fk_cooperativa__id=cooperativa_id)\
            .order_by(ordenar_por)
        categorias = Categoria.objects.all()
        cooperativas = Cooperativa.objects.all()

        return render(request, 'Cliente/index.html', {
            'productos_catalogo': producto_catalogo,
            'categorias': categorias,
            'cooperativas': cooperativas
        })


class Checkout(View):
    def get(self, request):
        # Obtenemos el carrito y sus items
        # Si no encontramos nada, redirijimos el usuario al home y le notificamos que no tiene items en el carrito
        # De lo contrario mostramos la página de checkout
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
        # Eliminamos el producto con el id dado del carrito de compras
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


class RegisterClientView(View):
    def get(self, request):
        return render(request, 'Cliente/registrar_cliente.html', {'form': ClientForm()})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre = cleaned_data.get('nombre')
            apellido = cleaned_data.get('apellido')
            contrasena = cleaned_data.get('contrasena')
            ciudad = cleaned_data.get('ciudad')
            departamento = cleaned_data.get('departamento')
            telefono_contacto = cleaned_data.get('telefono_contacto')
            correo = cleaned_data.get('correo')
            direccion = cleaned_data.get('direccion')
            numero_identificacion = cleaned_data.get('numero_identificacion')
            tipo_identificacion = cleaned_data.get('tipo_identificacion')

            user_model = User.objects.create_user(
                username=correo,
                password=contrasena,
                first_name=nombre,
                last_name=apellido,
                email=correo
            )
            user_model.save()
            cliente_model = Cliente(
                fk_django_user=user_model,
                ciudad=ciudad,
                departamento=departamento,
                telefono_contacto=telefono_contacto,
                direccion=direccion,
                numero_identificacion=numero_identificacion,
                tipo_identificacion=tipo_identificacion
            )
            cliente_model.save()
            return render(request, 'Cliente/index.html', {})
        else:
            return render_to_response('Cliente/registrar_cliente.html', {'form': form})
