from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^pedidos/$', views.pedidos, name='pedidos'),
    url(r'^pedidos/(?P<id_pedido>\d+)$', views.detallePedido, name='detallePedidos'),
    url(r'^pedidosUpdate/(?P<id_pedidoUpdate>\d+)$', views.actualizarEstadoPedido, name='actualizarEstadoPedido')
    #(?P<username>\w+) para recepcionar parametros desde el formulario d= digitos y w= string, el + signfica que se esperan una o mas

]
