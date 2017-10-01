# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class Index(View):
    def get(self, request):
        return render(request, 'Cliente/index.html', {})


class UpdateShoppingCart(View):
    def post(self, request):
        messages.add_message(request, messages.SUCCESS, 'El producto se agregó al carrito satisfactoriamente')
        return redirect(request.META.get('HTTP_REFERER', '/'))
