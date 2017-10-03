import django_tables2 as tables
from table.columns import Column
from Administrador.models import Pedido
from table import Table


class PedidoTable(Table):
    fecha_pedido = Column(field='fecha_pedido', header=u'Fecha del pedido')
    fecha_entrega = Column(field='fecha_entrega', header=u'Fecha de entrega del pedido')
    estado = Column(field='estado', header=u'Estado')
    valor_total = Column(field='valor_total', header=u'Valor total')

    class Meta:
        model = Pedido