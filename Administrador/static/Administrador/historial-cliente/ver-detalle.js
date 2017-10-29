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

// Cuando se haya cargaod la pagina se manda a mostar el mensaje de sin pedido pero
// este solo se activara si el cliente no tiene pedidos (Esta validacion se hace en el template).
$(document).ready(function(){
        $("#sinPedido").modal('show');
});

// Agrega el evento click al boton Aceptar del modal sin pedido.
// Permite cerrar el modal.
$('.cerrarSinPedido').click(function () {
    $("#sinPedido").modal('hide');
    $(".modal-backdrop").remove();
});

// Se captura el evento hide del modal sin pedido y  se redirige al usaurio a la pantalla
// de clientes - Administrador.
$('#sinPedido').on('hide.bs.modal', function (e) {
  $(location).attr('href','/administrador/clientes');
});
