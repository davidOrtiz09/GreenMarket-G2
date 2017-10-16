# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.http import JsonResponse


class Index(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'})
