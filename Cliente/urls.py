from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^ingresar$', views.Ingresar.as_view(), name='ingresar'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^checkout$', views.Checkout.as_view(), name='checkout'),

    url(r'^actualizar-carrito-compras$', views.UpdateShoppingCart.as_view(), name='actualizar-carrito-compras'),
    url(r'^eliminar-producto-carrito$', views.DeleteProductFromShoppingCart.as_view(), name='eliminar-producto-carrito'),

    url(r'^registrar-cliente$', views.RegisterClientView.as_view(), name='registrar-cliente'),
    url(r'^mis-pedidos$', views.MisPedidosView.as_view(), name='mis-pedidos'),
    url(r'^realizar-pago', views.DoPayment.as_view(), name='realizar-pago'),

    url(r'^canastas$', views.Canastas.as_view(), name='canastas'),
    url(r'^agregar-canasta-carrito$', views.AgregarCanastaCarrito.as_view(), name='agregar-canasta-carrito'),
    url(r'^eliminar-canasta-carrito$', views.EliminarCanastaCarritoCompras.as_view(), name='eliminar-canasta-carrito'),
    url(r'^actualizar-canasta-carrito-compras$', views.ActualizarCanastaCarritoCompras.as_view(), name='actualizar-canasta-carrito-compras'),

    url(r'^agregar-favorito$', views.AgregarProductoFavoritoView.as_view(), name='agregar-favorito'),
    url(r'^eliminar-favorito$', views.EliminarFavoritoView.as_view(), name='eliminar-favorito'),

    url(r'^detalle-mis-pedidos/(?P<id_pedido>\d+)$', views.DetalleMisPedidoView.as_view(), name='detalle-mis-pedidos'),
    url(r'^calificar-mis-pedidos/(?P<fk_pedido_producto>\d+)(?P<fk_productor>\d+)(?P<producto>\d+)(?P<pedido>\d+)$', views.CalificarMisPedidoView.as_view(), name='calificar-mis-pedidos'),
    url(r'^guardar-calificacion-mis-pedidos/(?P<pedido_producto>\d+)(?P<productor>\d+)(?P<id_pedido>\d+)$', views.InsertCalificacionProductoVew.as_view(), name='guardar-calificacion-mis-pedidos'),
    url(r'^mejores-productores', views.MejoresProductores.as_view(), name='mejores-productores'),

    url(r'^productos-sugeridos', views.ProductosSugeridos.as_view(), name='productos-sugeridos'),

]
