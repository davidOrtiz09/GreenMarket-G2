from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^actualizar-carrito-compras$', views.UpdateShoppingCart.as_view(), name='update-shoppping-cart')
]
