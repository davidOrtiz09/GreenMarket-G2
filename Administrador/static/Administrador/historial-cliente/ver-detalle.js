
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

 $(document).ready(function(){
        $("#sinPedido").modal('show');
});

$('.cerrarSinPedido').click(function () {
    $("#sinPedido").modal('hide');
    $(".modal-backdrop").remove();
});

$('#sinPedido').on('hide.bs.modal', function (e) {
  $(location).attr('href','/administrador/clientes');
});
