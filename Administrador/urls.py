from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^ingresar$', views.Ingresar.as_view(), name='ingresar'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^catalogo$', views.CatalogoView.as_view(), name='catalogo'),
    url(r'^pedidos/$', views.PedidosView.as_view(), name='pedidos'),
    url(r'^pedidos/(?P<id_pedido>\d+)$', views.DetallePedidoView.as_view(), name='detalle-pedido'),
    url(r'^actualizar-estado-pedido$', views.ActualizarEstadoPedidoView.as_view(), name='actualizar-estado-pedido'),
    url(r'^ofertas$', views.ListarOfertasView.as_view(), name='ofertas'),
    url(r'^ofertas/(?P<id_oferta>\d+)/(?P<guardado_exitoso>\d+)$', views.DetalleOfertaView.as_view(), name='detalle-ofertas'),
    url(r'^terminar-oferta$', views.RealizarOfertaView.as_view(), name='terminar-oferta'),
    url(r'^canastas$', views.Canastas.as_view(), name='canastas'),
    url(r'^elimimnar-canasta$', views.EliminarCanasta.as_view(), name='eliminar-canasta'),
    url(r'^crear-canasta$', views.CrearCanasta.as_view(), name='crear-canasta'),
    url(r'^publicar-canastas$', views.PublicarCanastas.as_view, name='publicar-canastas'),
    url(r'^canastas/(?P<id_canasta>\d+)$', views.DetallesCanasta.as_view(), name='detalles-canasta')
]
