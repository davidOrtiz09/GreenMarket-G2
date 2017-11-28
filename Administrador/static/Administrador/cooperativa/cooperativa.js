// Agrega el evento click al boton de ver deatlla de un pedido de un cliente.
// Ejecuta consulta para traer la cooperativas del sistema.
$('.seleccionCooperativas').click(function () {
       var id = $(this).attr('name');
        $.ajax({
            url: "/administrador/seleccion-cooperativa",
           context: document.body
        }).done(function(response) {
            var mdPedido = $("#selectCooperativa");
            mdPedido.html(response);
          mdPedido.modal('show');
        });
});

// Agrega el evento click al boton de volver del modal de seleccion de cooperativa.
// Permite cerrar el modal.
$('.cerrarModalCoop').click(function () {
    $("#selectCooperativa").modal('hide');
    $(".modal-backdrop").remove();
});
