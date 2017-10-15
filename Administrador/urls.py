from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^catalogo$', views.CatalogoView.as_view(), name='catalogo'),
    url(r'^pedidos$', views.PedidosView.as_view(), name='pedidos'),
    url(r'^pedidos/(?P<id_pedido>\d+)$', views.DetallePedidoView.as_view(), name='detalle-pedido'),
    url(r'^actualizar-estado-pedido$', views.ActualizarEstadoPedidoView.as_view(), name='actualizar-estado-edido'),
    url(r'^ofertas$', views.ListarOfertasView.as_view(), name='ofertas'),
    url(r'^ofertas/(?P<id_oferta>\d+)$', views.DetalleOfertaView.as_view(), name='detalle-ofertas'),
    url(r'^terminar-oferta$', views.RealizarOfertaView.as_view(), name='terminar-oferta')

    # (?P<username>\w+) para recepcionar parametros desde el formulario d= digitos y w= string, el + signfica que se
    # esperan una o mas

]
