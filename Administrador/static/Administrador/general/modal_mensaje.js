
// Cuando se haya cargaod la pagina se manda a mostar el mensaje de sin pedido pero
// este solo se activara si el cliente no tiene pedidos (Esta validacion se hace en el template).
$(document).ready(function(){
        $("#mensajeGeneral").modal('show');
});

// Agrega el evento click al boton Aceptar del modal sin pedido.
// Permite cerrar el modal.
$('.cerrarMensajeGeneral').click(function () {
    $("#mensajeGeneral").modal('hide');
    $(".modal-backdrop").remove();
});

// Se captura el evento hide del modal sin pedido y  se redirige al usaurio a la pantalla
// de clientes - Administrador.
$('#mensajeGeneral').on('hide.bs.modal', function (e) {
  $(location).attr('href',$('#url_ir').val());
});
