# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from operator import itemgetter
from django.contrib.auth.models import User
from django.db.models import Sum, Min, Max
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View
from Administrador.models import MejoresClientes
from django.views.decorators.csrf import csrf_exempt
from MarketPlace.models import Oferta_Producto, Catalogo, Producto, Pedido, PedidoProducto, Catalogo_Producto, \
    Productor, Oferta, Cooperativa, Canasta, Semana, Cliente, CanastaProducto, Orden_Compra
from Administrador.utils import catalogo_actual, catalogo_validaciones, obtener_valor_compra, obtener_cantidad_vendida
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from MarketPlace.utils import es_administrador, redirect_user_to_home, get_or_create_week
from django.db.transaction import atomic
from django.http import JsonResponse


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
                    subtitulo = semana.__str__
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
                       'semana_id': semana_id})

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
        for productor in Productor.objects.all():
            cantidad_ofertas = 0
            id_oferta = 0
            for oferta in Oferta.objects.filter(fk_productor=productor):
                cantidad_ofertas = Oferta_Producto.objects.filter(fk_oferta=oferta).count()
                id_oferta = oferta.id

            if cantidad_ofertas > 0:
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
        if aprobar == '0' and int(cantidad_aceptada) > 0:
            cantidad_aceptada = 0
        oferta_producto = Oferta_Producto.objects.get(pk=id_oferta_producto)
        oferta_producto.estado = aprobar
        oferta_producto.cantidad_aceptada = cantidad_aceptada
        oferta_producto.save()
        return redirect('administrador:detalle-ofertas', id_oferta=id_oferta, guardado_exitoso=1)


class Informes(View):
    def get(self, request):
        return render(request, 'Administrador/Informes/index.html', {})


class InformesClientesMasRentables(View):
    def get(self, request):
        mejores_clientes = list()
        for cliente in Cliente.objects.all():
            pedidos = Pedido.objects.filter(fk_cliente=cliente)
            cantidad_pedidos = pedidos.count()
            if cantidad_pedidos > 0:
                django_user = User.objects.get(id=cliente.fk_django_user_id)
                nombre = django_user.first_name + ' ' + django_user.last_name
                total_compras = pedidos.aggregate(Sum('valor_total'))
                ultima_fecha = pedidos.latest('fecha_pedido')
                mejores_clientes.append(
                    MejoresClientes(cliente.id, nombre, cantidad_pedidos, total_compras, ultima_fecha)
                )
        clientes_ordenados = sorted(mejores_clientes, key=lambda x: x.total_compras, reverse=True)
        return render(request, 'Administrador/Informes/clientes_mas_rentables.html', {
            'mejores_clientes': clientes_ordenados
        })


class SeleccionSemanas(View):
    def get(self, request):
        semanasAll = Semana.objects.all()
        semanasCount = len(semanasAll)
        semanas = []
        if semanasCount >= 4:
            semanas.append((semanasAll[semanasCount - 1]))
            semanas.append((semanasAll[semanasCount - 2]))
            semanas.append((semanasAll[semanasCount - 3]))
            semanas.append((semanasAll[semanasCount - 4]))
        else:
            semanas = semanasAll
        return render(request, 'Administrador/Informes/seleccionSemanas.html',
                      {'semanas': semanas})


class ObtenerMejoresProductos(View):
    def post(self, request):
        semanas = request.POST.getlist('semana', [])
        respuesta = []
        catalogoProd = Catalogo_Producto.objects.filter(fk_catalogo__fk_semana_id__in=semanas)
        for pro in catalogoProd:
            valor_compra = obtener_valor_compra(semanas, pro.fk_producto)
            valor_venta = pro.precio
            cantVendida = obtener_cantidad_vendida(semanas, pro.fk_producto)
            producto = Producto.objects.filter(id=pro.fk_producto_id).first()
            porcentaje = int
            if cantVendida != 0:
                porcentaje = int((((valor_venta - valor_compra) * cantVendida) * 100) / (valor_compra * cantVendida))
            else:
                porcentaje = 0
            respuesta.append({
                'producto': producto,
                'cantidad_vendida': cantVendida,
                'valor_compra': valor_compra,
                'valor_venta': valor_venta,
                'ganancia': (valor_venta - valor_compra) * cantVendida,
                'porcentaje': porcentaje

            })
        ordenado = sorted(respuesta, key=itemgetter('ganancia'), reverse=True)
        return render(request, 'Administrador/Informes/mejoresProductos.html', {'datos': ordenado})


class ClientesView(View):
    def get(self, request):
        return render(request, 'Administrador/clientes.html', {'clientes': Cliente.objects.all()})


class PerfilClienteView(View):
    def get(self, request, id):
        return render(request, 'Administrador/perfil-cliente.html', {'cliente': Cliente.objects.filter(id=id).first()})


class HistorialClienteView(View):
    # Retorna el template con todos los pedidos en orden descendentes pertenecientes a un cliente.
    def get(self, request, id):
        return render(request, 'Administrador/historial-cliente.html',
                      {'pedidos': Pedido.objects.filter(fk_cliente_id=id).order_by('fecha_pedido').reverse(),
                       'cliente': Cliente.objects.get(id=id)})


class PedidoClienteView(View):
    # Retorna el template con el detalle de un pedido en especifico.
    def get(self, request, id):
        return render(request, 'Administrador/_elements/_modal_pedido.html',
                      {'detallePedido': PedidoProducto.objects.filter(fk_pedido_id=id),
                       'pedidoId': id})


class Canastas(AbstractAdministradorLoggedView):
    def get(self, request):
        canastas = Canasta.objects.filter(fk_semana=get_or_create_week())
        return render(request, 'Administrador/canastas.html', {'canastas': canastas})


class DetallesCanasta(AbstractAdministradorLoggedView):
    def get(self, request, id_canasta):
        canasta = Canasta.objects.filter(id=id_canasta, fk_semana=get_or_create_week()).first()
        if canasta:
            ids_productos_canasta = CanastaProducto.objects \
                .filter(fk_canasta_id=canasta.id) \
                .values_list('fk_producto_catalogo_id', flat=True)

            productos_disponibles = Catalogo_Producto.objects \
                .filter(fk_catalogo__fk_semana_id=canasta.fk_semana_id) \
                .exclude(id__in=ids_productos_canasta) \
                .distinct()
            return render(request, 'Administrador/detalles-canasta.html', {
                'canasta': canasta, 'productos_disponibles': productos_disponibles
            })
        else:
            messages.add_message(request, messages.ERROR, 'No existe la canasta que estás buscando')
            return redirect(reverse('administrador:canastas'))

    @atomic
    def post(self, request, id_canasta):
        nombre = request.POST.get('nombre', '')
        imagen = request.FILES.get('imagen', None)

        canasta = Canasta.objects.filter(id=id_canasta).first()
        if canasta:
            canasta.nombre = nombre
            if imagen:
                canasta.imagen = imagen

            canasta.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Los datos principales de la canasta se actualizaron correctamente'
            )
            return redirect(reverse('administrador:detalles-canasta', kwargs={'id_canasta': canasta.id}))
        else:
            messages.add_message(request, messages.ERROR, 'No existe la canasta que estás buscando')
            return redirect(reverse('administrador:canastas'))


class EliminarCanasta(AbstractAdministradorLoggedView):
    @atomic
    def post(self, request):
        id_canasta = request.POST.get('id_canasta', '0')
        canasta = Canasta.objects.filter(id=id_canasta, fk_semana=get_or_create_week()).first()
        if canasta:
            canasta.delete()
            messages.add_message(request, messages.SUCCESS, 'La canasta fue eliminada')
        else:
            messages.add_message(request, messages.ERROR, 'No existe la canasta que estás tratando de eliminar')
        return redirect(reverse('administrador:canastas'))


class CrearCanasta(AbstractAdministradorLoggedView):
    def get(self, request):
        return render(request, 'Administrador/crear-canasta.html', {})

    @atomic
    def post(self, request):
        nombre = request.POST.get('nombre', '')
        imagen = request.FILES.get('imagen', None)
        nueva = Canasta(fk_semana=get_or_create_week(), nombre=nombre, imagen=imagen)
        nueva.save()
        messages.add_message(
            request, messages.SUCCESS,
            'La canasta fue creada exitosamente. Ahora puede agregar los productos que desee'
        )
        return redirect(reverse('administrador:detalles-canasta', kwargs={'id_canasta': nueva.id}))


class PublicarCanastas(AbstractAdministradorLoggedView):
    @atomic
    def post(self, request):
        canastas = Canasta.objects.filter(fk_semana=get_or_create_week())
        canastas.update(esta_publicada=True)
        messages.add_message(request, messages.SUCCESS, 'Las canastas fueron publicadas exitosamente')
        return redirect(reverse('administrador:canastas'))


class EliminarProductoCanasta(AbstractAdministradorLoggedView):
    @atomic
    def post(self, request):
        id_producto_canasta = request.POST.get('id_producto_canasta', '0')
        producto_canasta = CanastaProducto.objects.filter(id=id_producto_canasta).first()
        canasta = producto_canasta.fk_canasta
        if producto_canasta:
            producto_canasta.delete()
            messages.add_message(request, messages.SUCCESS, 'El producto fue eliminado de esta canasta')
        else:
            messages.add_message(request, messages.ERROR, 'El producto que desea elimimnar no existe en esta canasta')
        return redirect(reverse('administrador:detalles-canasta', kwargs={'id_canasta': canasta.id}))


class AgregarProductoCanasta(AbstractAdministradorLoggedView):
    @atomic
    def post(self, request, id_canasta):
        canasta = Canasta.objects.filter(id=id_canasta).first()
        if canasta:
            id_producto_catalogo = request.POST.get('id_producto_catalogo', '0')
            producto_catalogo = Catalogo_Producto.objects.filter(
                id=id_producto_catalogo,
                fk_catalogo__fk_semana_id=canasta.fk_semana_id
            ).first()

            if producto_catalogo:
                nuevo = CanastaProducto(
                    fk_canasta_id=canasta.id,
                    fk_producto_catalogo_id=producto_catalogo.id,
                    cantidad=1
                )
                nuevo.save()
                messages.add_message(request, messages.SUCCESS, 'El producto fue agregado a la canasta exitosamente')
            else:
                messages.add_message(request, messages.ERROR,
                                     'En el catalogo correspondiente de la cansata, no encontramos el producto que deseabas agregar')
            return redirect(reverse('administrador:detalles-canasta', kwargs={'id_canasta': canasta.id}))

        else:
            messages.add_message(request, messages.ERROR, 'No existe la canasta que estás tratando de editar')
            return redirect(reverse('administrador:canastas'))


class CambiarCantidadProductoCanasta(AbstractAdministradorLoggedView):
    @atomic
    def post(self, request):
        id_producto_canasta = request.POST.get('id_producto_canasta', '0')
        cantidad_str = request.POST.get('cantidad', '0')
        cantidad = int(cantidad_str)
        producto_canasta = CanastaProducto.objects.filter(id=id_producto_canasta).first()
        canasta = producto_canasta.fk_canasta
        if producto_canasta:
            producto_canasta.cantidad = cantidad if cantidad > 0 else 1
            producto_canasta.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'La cantidad del producto {producto} fue actualziado en esta canasta'
                    .format(producto=producto_canasta.nombre_producto)
            )

        return redirect(reverse('administrador:detalles-canasta', kwargs={'id_canasta': canasta.id}))


class Productores(AbstractAdministradorLoggedView):
    def get(self, request):
        productores = Productor.objects.all().order_by('id')
        return render(request, 'Administrador/Productores.html', {'listaProductores': productores})


class CrearProductor(AbstractAdministradorLoggedView):
    def get(self, request):
        return render(request, 'Administrador/crear-productor.html', {})


class GetDepartamentos(View):
    def get(self, request):
        departamentos = Cooperativa.objects.all().values('departamento').distinct('departamento')
        return JsonResponse({"ListaDepartamentos": list(departamentos)})


class GetCiudadPorDepto(View):
    def get(self, request):
        idDepto = request.GET['idDepto']
        ciudades = Cooperativa.objects.filter(departamento=idDepto).values('ciudad').distinct('ciudad')
        return JsonResponse({"ListaCiudades": list(ciudades)})


class GetCooperativaPorCiudad(View):
    def get(self, request):
        idCooperativa = request.GET['ciudad']
        cooperativas = Cooperativa.objects.filter(ciudad=idCooperativa).values('nombre', 'id')
        return JsonResponse({"ListaCooperativas": list(cooperativas)})


@method_decorator(csrf_exempt, name='dispatch')
class AgregarProductor(AbstractAdministradorLoggedView):
    def get(self, request):
        return JsonResponse({})

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        cooperativa = Cooperativa.objects.filter(id=body["cooperativaId"]).first()

        nombre = body["nombre"]
        apellido = body["apellido"]
        contrasena = body["contrasena"]
        correo = body["correo"]

        direccion = body["direccion"]
        descripcion = body["descripcion"]
        coordenadas = body["coordenadas"]

        user_model = User.objects.create_user(
            username=correo,
            password=contrasena,
            first_name=nombre,
            last_name=apellido,
            email=correo
        )
        user_model.save()
        productor_model = Productor(
            fk_django_user=user_model,
            fk_cooperativa=cooperativa,
            nombre=nombre,
            direccion=direccion,
            descripcion=descripcion,
            coordenadas_gps=coordenadas
        )
        productor_model.save()
        return JsonResponse({"Mensaje": "Finalizó con exito"})


class ConsultarPagosPendientes(View):
    def get(self, request):
        ofertas_por_pagar = Oferta_Producto.objects.filter(fk_orden_compra__isnull=True) \
            .distinct('fk_oferta__fk_productor')
        productor = Productor.objects.all()

        return render(request, 'Administrador/pagos-pendientes-productor.html',
                      {'ofertas_por_pagar': ofertas_por_pagar,
                       'productores': productor})


class DetalleOrdenPagoProductores(View):
    def get(self, request, id_productor):
        ofertas_por_pagar = Oferta_Producto.objects.filter(fk_orden_compra__isnull=True,
                                                           fk_oferta__fk_productor_id=id_productor)

        productor = Productor.objects.filter(id=id_productor)[0]
        return render(request, 'Administrador/detalle-productos-orden-pago.html', {
            'ofertas_por_pagar': ofertas_por_pagar,
            'productor': productor
        })


class GenerarOrdenPagoProductores(View):
    def post(self, request):
        orden_compra_Json = json.loads(request.POST.get('orden-pago-form'))
        orden_compra = orden_compra_Json.get('orden_compra')
        valor_total_json = orden_compra.get('valor_total')
        productor = Productor.objects.filter(id=orden_compra.get('productor_id'))[0]
        orden_compra = Orden_Compra.objects \
            .create(fk_productor=productor, valor_total=valor_total_json, estado='PA')

        for oferta_producto in orden_compra_Json.get('oferta_productos'):
            ofertas_por_pagar = Oferta_Producto.objects.filter(id=oferta_producto.get('oferta_profucto'))[0]
            ofertas_por_pagar.fk_orden_compra = orden_compra
            ofertas_por_pagar.save()

        return render(request, 'Administrador/detalle-orden-pago.html', {
            'ofertas_producto': Oferta_Producto.objects.filter(fk_orden_compra=orden_compra)
        })

    def get(self, request):
        productores_pagar = Oferta_Producto.objects.filter(fk_orden_compra__isnull=True) \
            .distinct('fk_oferta__fk_productor')

        for productor in productores_pagar:
            pagar_ofertas = Oferta_Producto.objects.filter(fk_orden_compra__isnull=True,
                                                           fk_oferta__fk_productor=productor.fk_oferta.fk_productor)

            valor_total = pagar_ofertas.aggregate(Sum('precioProvedor')).get('precioProvedor__sum')
            orden_compra = Orden_Compra.objects \
                .create(fk_productor=productor.fk_oferta.fk_productor, valor_total=valor_total, estado='PA')

            for pagar_oferta in pagar_ofertas:
                pagar_oferta.fk_orden_compra = orden_compra
                pagar_oferta.save()

        return render(request, 'Administrador/pagos-pendientes-productor.html',
                      {'ofertas_por_pagar': productores_pagar,
                       'productores': Productor.objects.all()})


class OrdenesPagoProductores(View):
    def get(self, request, id_productor):
        orden_compra = Orden_Compra.objects.filter(fk_productor=id_productor).order_by('-id')
        return render(request, 'Administrador/ordenes-pago-productor.html',
                      {'ordenes_compra': orden_compra})


class DetalleOrdenPago(View):
    def get(self, request, orden_compra_id):
        orden_compra = Orden_Compra.objects.filter(id=orden_compra_id)

        ofertas_producto = Oferta_Producto.objects. \
            filter(fk_orden_compra=orden_compra)
        return render(request, 'Administrador/detalle-orden-pago.html', {
            'ofertas_producto': ofertas_producto
        })
