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
    url(r'^favoritos$', views.FavoritoView.as_view(), name='favoritos'),

]
