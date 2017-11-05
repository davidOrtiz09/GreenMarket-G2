$(document).ready(function () {
    actualizarTotalPagar();
    TotalPagar();
});


$('button#ordenPago').click(function () {

    console.log("ingrese a La fucnion de pago 2");
    var container = $('div#orden-Pago-detalle');
    var response = [];
    var oferta_productos = [];
    var orden_compra = [];
    var productRows = container.find('tr.product-orden-pago');
    var productor_id = container.find('input.productor-id').val();
    var inputTotalPagar = container.find('input.total-a-pagar').val();
    for (var i = 0; i < productRows.length; i++) {
        var row = $(productRows[i]);
        var productId = row.find('input.oferta-producto-id').val();
        if (row.find('input.check-pago').is(':checked')) {
            oferta_productos.push({
                oferta_profucto: productId
            })
        }

    }
    orden_compra={
                valor_total: inputTotalPagar,
                productor_id: productor_id
            }

    response={
                orden_compra: orden_compra,
                oferta_productos: oferta_productos
            }

    var formJson = response;
    var stringPago = JSON.stringify(formJson);
    var form = $('form#form-orden-pago');
    var inputJson = form.find('input#json-form-orden');
    inputJson.val(stringPago);
    form.submit();
});


$('input.change-check').change(function () {

    actualizarTotalPagar()

});


function actualizarTotalPagar() {

    var detallesPedido = $('div#orden-Pago-detalle');
    var spanTotalPagarToCop = detallesPedido.find('span#total-a-pagar-tocop');
    var inputTotalPagar = detallesPedido.find('input.total-a-pagar');
    var productRows = detallesPedido.find('tr.product-orden-pago');
    var totalPagar = 0;
    for (var i = 0; i < productRows.length; i++) {
        var row = $(productRows[i]);
        if (row.find('input.check-pago').is(':checked')) {
            var priceProductor = parseFloat(row.find('input.price-productor').val());
            totalPagar += priceProductor
        }
    }
    inputTotalPagar.val(totalPagar)
    spanTotalPagarToCop.html(toCop(totalPagar));

}

function TotalPagar() {

    var detallesPedido = $('div#orden-Pago-detalle');
    var spanTotalPagarToCop = detallesPedido.find('span#total-a-pagar-tocop');
    var productRows = detallesPedido.find('tr.product-orden-pago');
    var totalPagar = 0;
    for (var i = 0; i < productRows.length; i++) {
        var row = $(productRows[i]);
            var priceProductor = parseFloat(row.find('input.price-productor').val());
            totalPagar += priceProductor
    }
    spanTotalPagarToCop.html(toCop(totalPagar));

}
