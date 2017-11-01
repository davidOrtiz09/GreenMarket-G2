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
    # (?P<username>\w+) para recepcionar parametros desde el formulario d= digitos y w= string, el + signfica que se
    # esperan una o mas
    url(r'^informes$', views.Informes.as_view(), name='informes'),
    url(r'^informes/clientes-mas-rentables$', views.InformesClientesMasRentables.as_view(),
        name='informes/clientes-mas-rentables'),
    url(r'^informes/seleccionSemanas', views.seleccionSemanas.as_view(), name='informes/seleccionSemanas'),
    url(r'^informes/obtener_mejores_productos', views.obtener_mejores_productos.as_view(), name='informes/obtener_mejores_productos'),
]
