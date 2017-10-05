from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^checkout$', views.Checkout.as_view(), name='checkout')
]
