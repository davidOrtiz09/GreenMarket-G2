from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^crear-oferta', views.crear_oferta, name='crearOferta'),
    url(r'^getCategorias/$', views.get_categorias_view, name='GetCategorias'),
    url(r'^getProductosPorCategoria/$', views.get_productos_por_categoria, name='getProductosPorCategoria'),
    url(r'^agregarOfertaProductor/$', views.agregar_oferta_productor, name='agregarOfertaProductor')
]
