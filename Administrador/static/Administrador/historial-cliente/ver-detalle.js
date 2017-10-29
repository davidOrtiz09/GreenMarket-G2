
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

$('.cerrarDetalle').click(function () {
    $("#detallePedido").modal('hide');
    $(".modal-backdrop").remove();
});