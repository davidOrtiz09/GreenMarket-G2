// Agrega el evento click al boton de ver deatlla de un pedido de un cliente.
// Ejecuta consulta para traer el detalle del pedido y activa el modal para mostrar la informacion.
$('.verDetalle').click(function () {
       var id = $(this).attr('name');
        $.ajax({
            url: "/administrador/historial-cliente/pedido/"+id,
           context: document.body
        }).done(function(response) {
            var mdPedido = $("#detallePedido");
            mdPedido.html(response);
          mdPedido.modal('show');
        });
});

// Agrega el evento click al boton de volver del modal un pedido de un cliente.
// Permite cerrar el modal.
$('.cerrarDetalle').click(function () {
    $("#detallePedido").modal('hide');
    $(".modal-backdrop").remove();
});
