# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, render_to_response
from django.views import View
from django.contrib import messages
from Cliente.forms import ClientForm, PaymentForm
from MarketPlace.models import Cliente, Catalogo_Producto, Categoria, Cooperativa, Pedido, PedidoProducto, \
    Oferta_Producto
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import F
import json


class Index(View):
    def get(self, request):
        cooperativas = Cooperativa.objects.all()
        producto_catalogo = Catalogo_Producto.objects \
            .filter(fk_catalogo__fk_cooperativa_id=cooperativas.first()) \
            .order_by('fk_producto__nombre')
        categorias = Categoria.objects.all()
        return render(request, 'Cliente/index.html', {
            'productos_catalogo': producto_catalogo,
            'categorias': categorias,
            'cooperativas': cooperativas
        })

    def post(self, request):
        # Se listan los productos por Cooperativa y se ordenan segun filtro
        cooperativa_id = request.POST.get('cooperativa_id', '')
        ordenar_por = request.POST.get('ordenar', '')
        producto_catalogo = Catalogo_Producto.objects \
            .filter(fk_catalogo__fk_cooperativa__id=cooperativa_id) \
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
        product = Catalogo_Producto.objects.get(id=product_id)
        if product_id > 0 and quantity != 0:
            cart = request.session.get('cart', None)
            if not cart:
                cart = {
                    'items': [{
                        'product_id': product_id,
                        'quantity': quantity,
                        'name': product.fk_producto.nombre,
                        'image': product.fk_producto.imagen.url,
                        'price': float(product.precio),
                        'unit': product.fk_producto.unidad_medida
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
                        'quantity': quantity,
                        'name': product.fk_producto.nombre,
                        'image': product.fk_producto.imagen.url,
                        'price': float(product.precio),
                        'unit': product.fk_producto.unidad_medida
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


class MisPedidosView(View):
    def get(self, request):
        user_model = User.objects.get(username=request.user.username)
        cliente = Cliente.objects.filter(fk_django_user=user_model)
        pedidos_cliente = Pedido.objects.filter(fk_cliente=cliente)
        return render(request, 'Cliente/mis_pedidos.html', {
            'pedidos_entregados': pedidos_cliente.filter(estado='EN'),
            'pedidos_por_entregar': pedidos_cliente.filter(estado__in=('PE', 'EC'))
        })


class DoPayment(View):
    def get(self, request):
        return render(request, 'Cliente/checkout/checkout.html', {'form': PaymentForm()})

    def post(self, request):
        checkout_Json = json.loads(request.POST.get('checkout_form'))
        detalles_pedido = checkout_Json.get('detalles_pedido')
        informacion_envio = checkout_Json.get('informacion_envio')
        informacion_pago = checkout_Json.get('informacion_pago')
        nombre_envio = informacion_envio.get('nombre')
        direccion_envio = informacion_envio.get('direccion')
        email_envio = informacion_envio.get('email')
        celular_envio = informacion_envio.get('celular')
        telefono_envio = informacion_envio.get('telefono')
        observaciones_envio = informacion_envio.get('observaciones')
        nombre_pago = informacion_pago.get('nombre_completo')
        numero_identificacion = informacion_pago.get('numero_documento')
        tipo_identificacion = informacion_pago.get('tipo_documento')

        user_model = User.objects.get(username=request.user.username)
        cliente_model = Cliente.objects.get(fk_django_user=user_model)
        pedido_model = Pedido(
            fk_cliente=cliente_model,
            fecha_pedido=datetime.now(),
            fecha_entrega=datetime.now(),
            estado='PE',
            valor_total=0,
            nombre_envio=nombre_envio,
            direccion_envio=direccion_envio,
            email_envio=email_envio,
            telefono_envio=telefono_envio,
            observaciones_envio=observaciones_envio,
            nombre_pago=nombre_pago,
            tipo_identificacion=tipo_identificacion,
            numero_identificacion=numero_identificacion
        )

        pedido_model.save()

        valor_total = 0
        for item in detalles_pedido:
            producto_catalogo = Catalogo_Producto.objects.get(id=item.get('product_id'))
            cantidad = int(item.get('quantity'))
            pedido_producto_model = PedidoProducto(
                fk_catalogo_producto=producto_catalogo,
                fk_pedido=pedido_model,
                cantidad=cantidad
            )
            pedido_producto_model.save()
            valor_total += producto_catalogo.precio * cantidad
            cantidad_disponible = 0
            while cantidad != 0:
                if cantidad_disponible > cantidad:
                    oferta_producto.cantidad_vendida = cantidad
                    oferta_producto.save()
                    cantidad = 0

                elif cantidad_disponible > 0:
                    oferta_producto.cantidad_vendida = oferta_producto.cantidad_aceptada
                    oferta_producto.save()
                    cantidad = cantidad - cantidad_disponible
                else:
                    oferta_producto = Oferta_Producto \
                        .objects.filter(fk_producto=producto_catalogo.fk_producto) \
                        .exclude(cantidad_vendida=F('cantidad_aceptada')) \
                        .order_by('precioProvedor').first()
                    cantidad_disponible = oferta_producto.cantidad_aceptada - oferta_producto.cantidad_vendida

        request.session['cart'] = ''
        pedido_model.valor_total = valor_total
        pedido_model.save()

        return render(request, 'Cliente/mis_pedidos.html',
                      {'compra': True})
