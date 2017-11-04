from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^ingresar$', views.Ingresar.as_view(), name='ingresar'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^catalogo$', views.CatalogoSemanasView.as_view(), name='catalogo-semanas'),
    url(r'^catalogo/semana/(\d+)/$', views.CatalogoView.as_view(), name='catalogo'),
    url(r'^pedidos/$', views.PedidosView.as_view(), name='pedidos'),
    url(r'^pedidos/(?P<id_pedido>\d+)$', views.DetallePedidoView.as_view(), name='detalle-pedido'),
    url(r'^actualizar-estado-pedido$', views.ActualizarEstadoPedidoView.as_view(), name='actualizar-estado-pedido'),
    url(r'^ofertas$', views.ListarOfertasView.as_view(), name='ofertas'),
    url(r'^ofertas/(?P<id_oferta>\d+)/(?P<guardado_exitoso>\d+)$', views.DetalleOfertaView.as_view(), name='detalle-ofertas'),
    url(r'^terminar-oferta$', views.RealizarOfertaView.as_view(), name='terminar-oferta'),
    url(r'^informes$', views.Informes.as_view(), name='informes'),
    url(r'^informes/clientes-mas-rentables$', views.InformesClientesMasRentables.as_view(),
        name='informes/clientes-mas-rentables'),
    url(r'^informes/seleccionSemanas', views.SeleccionSemanas.as_view(), name='informes/seleccionSemanas'),
    url(r'^informes/obtener_mejores_productos', views.ObtenerMejoresProductos.as_view(), name='informes/obtener_mejores_productos'),
    url(r'^clientes$', views.ClientesView.as_view(), name='clientes'),
    url(r'^clientes/(\d+)/$', views.PerfilClienteView.as_view(), name='perfil_cliente'),
    url(r'^historial-cliente$', views.HistorialClienteView.as_view(), name='historial-cliente'),
    url(r'^historial-cliente/(\d+)/$', views.HistorialClienteView.as_view(), name='historial-cliente'),
    url(r'^historial-cliente/pedido/(\d+)/$', views.PedidoClienteView.as_view(), name='pedido'),

    url(r'^canastas$', views.Canastas.as_view(), name='canastas'),
    url(r'^elimimnar-canasta$', views.EliminarCanasta.as_view(), name='eliminar-canasta'),
    url(r'^crear-canasta$', views.CrearCanasta.as_view(), name='crear-canasta'),
    url(r'^publicar-canastas$', views.PublicarCanastas.as_view, name='publicar-canastas'),
    url(r'^canastas/(?P<id_canasta>\d+)$', views.DetallesCanasta.as_view(), name='detalles-canasta'),
    url(r'^eliminar-producto-canasta$', views.EliminarProductoCanasta.as_view(), name='eliminar-producto-canasta'),
    url(r'^cambiar-cantidad-producto-canasta$', views.CambiarCantidadProductoCanasta.as_view(),name='cambiar-cantidad-producto-canasta'),
]
