# -*- coding: utf-8 -*-
import datetime
from MarketPlace.models import Catalogo, Semana, Cooperativa


# Se obtiene el catalogo más reciente creado
def catalogo_actual():
    catalogo = Catalogo.objects.order_by('-fecha_creacion').first()
    ofertas_pro = []
    if catalogo is not None:
        ofertas_pro = catalogo.catalogo_producto_set.values('fk_producto',
                                                            'fk_producto__nombre',
                                                            'fk_producto__imagen',
                                                            'fk_producto__unidad_medida',
                                                            'precio')
        subtitulo = catalogo.fk_semana.fecha_inicio.strftime("%d/%m/%y") + ' - ' + catalogo.fk_semana.fecha_fin.strftime("%d/%m/%y")
    else:
        subtitulo = 'No hay catálago disponible'

    return {'ofertas_pro': ofertas_pro, 'subtitulo': subtitulo}


def catalogo_validaciones(semana_id):
    # Se valida que exista una semana activa para la fecha actual
    fecha_actual = datetime.date.today()
    semana = Semana.objects.filter(id=semana_id).first()
    if(semana is None):
        return {'mensaje': 'No existe la semana seleccionada en el sistema.'}

    # Se valida que exista por lo menos una cooperativa.
    cooperativa = Cooperativa.objects.first()
    if (cooperativa is None):
        return {'mensaje': 'No hay cooperativas registradas en el sistema!'}

    return({'mensaje': '',
            'semana':semana, 'cooperativa': cooperativa})
