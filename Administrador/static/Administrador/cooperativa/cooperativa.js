
var URLDomain = document.location.origin+"/";
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
    cerrarModalCooperativas();
});


function cerrarModalCooperativas(idCooperativa) {
    $("#selectCooperativa").modal('hide');
    $(".modal-backdrop").remove();
}
function clicCooperativa(idCooperativa) {

    jsonCooperativa = {"idCooperativa":idCooperativa};

    $.ajax({
        url: URLDomain + "administrador/seleccion-cooperativa/fijar",
        data: JSON.stringify(jsonCooperativa),
        type: 'POST',
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function (data) {
            cerrarModalCooperativas();
            if(data.Mensaje === "OK") {
                location.reload();
            }
        },
        failure: function (errMsg) {
            alert('Se presentó un error. No se pudó seleccionar la cooperativa.');
            cerrarModalCooperativas();
            location.reload();
        }
    });
}
