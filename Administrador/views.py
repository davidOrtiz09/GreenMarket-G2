# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.db.models import Sum, Min, Max, QuerySet
from django.shortcuts import render, redirect, reverse
from django.views import View
from MarketPlace.models import Oferta_Producto, Catalogo, Producto, Pedido, PedidoProducto, Catalogo_Producto, \
    Productor, Oferta, Cooperativa, Semana, Cliente
from Administrador.utils import catalogo_actual, catalogo_validaciones
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from MarketPlace.utils import es_administrador, redirect_user_to_home


class AbstractAdministradorLoggedView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if es_administrador(self.request.user):
                return super(AbstractAdministradorLoggedView, self).dispatch(*args, **kwargs)
            else:
                return redirect_user_to_home(self.request)
        else:
            return redirect(reverse('administrador:ingresar'))


class Ingresar(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('administrador:index'))
        else:
            return render(request, 'Administrador/ingresar.html', {})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('administrador:index'))
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None and es_administrador(user):
                login(request, user)
                return redirect(reverse('administrador:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Por favor verifica tu usuario y contraseña')
                return render(request, 'Administrador/ingresar.html', {})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('administrador:ingresar'))


class Index(AbstractAdministradorLoggedView):
    def get(self, request):
        return render(request, 'Administrador/index.html', {})

class CatalogoSemanasView(AbstractAdministradorLoggedView):
    def get(self, request):

        return render(request, 'Administrador/catalogo-semanas.html',
                      {'semanas': Semana.objects.all().order_by('-fecha_inicio')})


class CatalogoView(AbstractAdministradorLoggedView):
    def get(self, request, semana_id):
        info_catalogo = {}
        oferta_nueva = False

        resp = catalogo_validaciones(semana_id)


        if (resp['mensaje'] == ''):
            semana = resp['semana']

            # Se valida que no se haya creado ya un catalogo para la semana.
            catalogo = Catalogo.objects.filter(fk_semana_id=semana_id).first()
            if catalogo is None:
                # Se obtienen las ofertas agrupadas por producto (cantidad, precio minimo y maximo)
                # Solo se toman las ofertas aceptadas y correspondientes a la semana.
                ofertas_pro = Oferta_Producto \
                    .objects.filter(estado=1, fk_oferta__fk_semana_id=semana_id) \
                    .values('fk_producto', 'fk_producto__nombre', 'fk_producto__imagen', 'fk_producto__unidad_medida') \
                    .annotate(preMin=Min('precioProvedor'), preMax=Max('precioProvedor'),
                              canAceptada=Sum('cantidad_aceptada')) \
                    .distinct()

                oferta_nueva = ofertas_pro.count() > 0

                if oferta_nueva:
                    subtitulo = semana.fecha_inicio.strftime("%d/%m/%y") + '-' + semana.fecha_fin.strftime("%d/%m/%y")
                else:
                    subtitulo = "No hay ofertas disponibles para crear el catálogo"

                info_catalogo.update({'ofertas_pro': ofertas_pro, 'subtitulo': subtitulo})
            else:
                # Se muestra el catalogo ya creado.
                info_catalogo = catalogo_actual()
        else:
            info_catalogo.update({'ofertas_pro': [], 'subtitulo': resp['mensaje']})

        return render(request, 'Administrador/catalogo.html',
                      {'ofertas_pro': info_catalogo['ofertas_pro'],
                       'subtitulo': info_catalogo['subtitulo'],
                       'oferta_nueva': oferta_nueva,
                       'semana_id':semana_id})

    def post(self, request, semana_id):
        # Se carga la información desde el JSON recibido donde viene el id del producto con su respectivo precio.
        precios_recibidos = json.loads(request.POST.get('precios_enviar'))

        # Se crea el catalogo
        fecha_cierre = datetime.date.today() + datetime.timedelta(days=3)
        catalogo = Catalogo.objects.create(fk_semana_id=semana_id, fecha_cierre=fecha_cierre)
        catalogo.save()

        # Se agregan los  productos al catalogo
        for item in precios_recibidos:
            Catalogo_Producto.objects.create(fk_catalogo=catalogo,
                                             fk_producto=Producto(id=item['producto']),
                                             precio=item['precio'])

        # Se carga la informacion del catalogo creado
        info_catalogo = catalogo_actual()
        subtitulo = "Catálogo creado correctamente!\r\n" + info_catalogo['subtitulo']

        return render(request, 'Administrador/catalogo.html', {
            'ofertas_pro': info_catalogo['ofertas_pro'],
            'subtitulo': subtitulo,
            'oferta_nueva': False
        })


class PedidosView(AbstractAdministradorLoggedView):
    def get(self, request):
        return render(request, 'Administrador/pedidos.html', {'pedidos': Pedido.objects.all()})

    def post(self, request):
        if request.POST.get('fecha_inicio', '') == '':
            fecha_inicio = datetime.datetime.now()
            fecha_fin = datetime.datetime.now()
            pedidos = Pedido.objects.filter(fecha_pedido__gte=fecha_inicio, fecha_pedido__lte=fecha_fin)
        else:
            fecha_inicio = request.POST.get('fecha_inicio', '')
            fecha_fin = request.POST.get('fecha_fin', '')
            pedidos = Pedido.objects.filter(fecha_pedido__gte=fecha_inicio, fecha_pedido__lte=fecha_fin)

        return render(request, 'Administrador/pedidos.html', {'pedidos': pedidos})


class DetallePedidoView(AbstractAdministradorLoggedView):
    def get(self, request, id_pedido):
        detalle_pedido = PedidoProducto.objects.filter(fk_pedido=id_pedido)
        pedido = Pedido.objects.get(id=id_pedido)
        if pedido.estado != 'PE':
            disable_button = 'disabled'
        else:
            disable_button = ''
        return render(request, 'Administrador/detalle-pedido.html', {
            'detalle_pedido': detalle_pedido,
            'id_pedido': id_pedido,
            'disable_button': disable_button
        })


class ActualizarEstadoPedidoView(AbstractAdministradorLoggedView):
    def post(self, request):
        id_pedido = request.POST.get('id_pedido', '0')
        pedido = Pedido.objects.get(id=id_pedido)
        pedido.estado = 'EC'
        pedido.save()
        return render(request, 'Administrador/pedidos.html', {'pedidos': Pedido.objects.all()})


class ListarOfertasView(AbstractAdministradorLoggedView):
    def get(self, request):
        ofertas = list()
        cantidad_ofertas = 0
        id_oferta = 0
        for productor in Productor.objects.all():
            for oferta in Oferta.objects.filter(fk_productor=productor.id):
                cantidad_ofertas = Oferta_Producto.objects.filter(fk_oferta=oferta.id).count()
                id_oferta = oferta.id
            ofertas.append((productor.nombre, cantidad_ofertas, id_oferta))

        return render(request, 'Administrador/ofertas.html', {'ofertas': ofertas})


class DetalleOfertaView(AbstractAdministradorLoggedView):
    def get(self, request, id_oferta, guardado_exitoso):
        ofertas_producto = Oferta_Producto.cargar_ofertas(id_oferta)

        return render(request, 'Administrador/detalle-oferta.html', {
            'ofertas_producto': ofertas_producto,
            'id_oferta': id_oferta,
            'guardado_exitoso': guardado_exitoso
        })


class RealizarOfertaView(AbstractAdministradorLoggedView):
    def post(self, request):
        id_oferta = request.POST.get('id_oferta')
        id_oferta_producto = request.POST.get('id_oferta_producto')
        aprobar = request.POST.get('aprobar')
        cantidad_aceptada = request.POST.get('cantidad_aceptada')
        if aprobar == '0' and cantidad_aceptada > 0:
            cantidad_aceptada = 0
        oferta_producto = Oferta_Producto.objects.get(pk=id_oferta_producto)
        oferta_producto.estado = aprobar
        oferta_producto.cantidad_aceptada = cantidad_aceptada
        oferta_producto.save()
        return redirect('administrador:detalle-ofertas', id_oferta=id_oferta, guardado_exitoso=1)

class ClientesView(View):
    def get(self, request):

        return render(request, 'Administrador/clientes.html', {'clientes':Cliente.objects.all()})

class HistorialClienteView(View):
    # Retorna el template con todos los pedidos en orden descendentes pertenecientes a un cliente.
    def get(self, request, id):

        return render(request, 'Administrador/historial-cliente.html',
                      {'pedidos':Pedido.objects.filter(fk_cliente_id=id).order_by('fecha_pedido').reverse(),
                       'cliente':Cliente.objects.get(id=id)})
class PedidoClienteView(View):
    # Retorna el template con el detalle de un pedido en especifico.
    def get(self, request, id):
        return render(request, 'Administrador/_elements/_modal_pedido.html',
                      {'detallePedido':PedidoProducto.objects.filter(fk_pedido_id=id),
                       'pedidoId':id})
