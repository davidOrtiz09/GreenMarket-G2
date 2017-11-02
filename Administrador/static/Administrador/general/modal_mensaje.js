
// Cuando se haya cargaod la pagina se manda a mostar el modal general.
// Solo se mostrara bajo la condicion que se haya colocado en el template que se utiliza.
$(document).ready(function(){
        $("#mensajeGeneral").modal('show');
});

// Agrega el evento click al boton Aceptar del modal general.
// Permite cerrar el modal.
$('.cerrarMensajeGeneral').click(function () {
    $("#mensajeGeneral").modal('hide');
    $(".modal-backdrop").remove();
});

// Se captura el evento hide del modal general y  se redirige a la pantalla indicado en url_ir.
$('#mensajeGeneral').on('hide.bs.modal', function (e) {
  $(location).attr('href',$('#url_ir').val());
});
