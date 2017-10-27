from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^ingresar$', views.Ingresar.as_view(), name='ingresar'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^productos-vendidos$', views.ProductosVendidosView.as_view(), name='productos-vendidos'),
    url(r'^crear-oferta', views.CrearOferta.as_view(), name='crearOferta'),
    url(r'^getCategorias/$', views.GetCategorias.as_view(), name='GetCategorias'),
    url(r'^getProductosPorCategoria/$', views.GetProductorPorCategoria.as_view(), name='getProductosPorCategoria'),
    url(r'^agregarOfertaProductor/$', views.AgregarOferta.as_view(), name='agregarOfertaProductor')
]
