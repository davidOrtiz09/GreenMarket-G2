# -*- coding: utf-8 -*-
from MarketPlace.models import Catalogo


# Se obtiene el catalogo más reciente creado
def catalogo_actual():
    catalogo = Catalogo.objects.order_by('-fecha_creacion').first()
    ofertas_pro = []
    if catalogo is not None:
        ofertas_pro = catalogo.catalogo_producto_set.values('fk_producto',
                                                            'fk_producto__nombre',
                                                            'fk_producto__imagen',
                                                            'precio')
        subtitulo = catalogo.fecha_creacion.strftime("%d/%m/%y") + ' - ' + catalogo.fecha_cierre.strftime("%d/%m/%y")
    else:
        subtitulo = 'No hay catálago disponible'

    return {'ofertas_pro': ofertas_pro, 'subtitulo': subtitulo}
