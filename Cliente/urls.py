from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^checkout$', views.Checkout.as_view(), name='checkout'),
    url(r'^actualizar-carrito-compras$', views.UpdateShoppingCart.as_view(), name='actualizar-carrito-compras'),
    url(r'^eliminar-producto-carrito', views.DeleteProductFromShoppingCart.as_view(), name='eliminar-producto-carrito')
]
