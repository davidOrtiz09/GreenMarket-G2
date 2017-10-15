from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^productos-vendidos$', views.ProductosVendidosView.as_view(), name='productos-vendidos'),
]
