$(document).ready(function () {
    actualizarTotalPagar();
    TotalPagar();
});


$('button#ordenPago').click(function () {

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
/*
    Se formatea un número a moneda para que sea más legible
 */
function toCop(number){
    return number.toLocaleString('en-us', {minimumFractionDigits: 0 });
}

function modificarCanastaProducto(selector_input, cantidad){
    var input = $(selector_input);
    var valorActual = parseInt(input.val());
    var max = input.attr('max');
    var nuevoValor = valorActual + cantidad;
    if(nuevoValor >= 1 && nuevoValor <= max){
        input.val(nuevoValor);
    }

}

function modificarCanastaInput(selector_input, nuevoValor){
    var input = $(selector_input);
    var max = input.attr('max');
    var intNuevoValor = parseInt(nuevoValor);
    if(intNuevoValor < 1){
        input.val(1);
    }
    if(intNuevoValor > max){
        input.val(max);
    }
}

$('button#sugerirProductos').click(function () {

    var container = $('div#sugerir-productos-div');
    var response = [];
    var configuracion = [];
    var sugerir_productos = [];
    var productRows = container.find('tr.sugerir-producto-tr');
    for (var i = 0; i < productRows.length; i++) {
        var row = $(productRows[i]);
        var productId = row.find('input.oferta-producto-id').val();
        if (row.find('input.check-sugerir').is(':checked')) {
            sugerir_productos.push({
                productos: productId
            })
        }

    }


    var conservar = container.find('input.conservar').is(':checked');
    var reemplazar = container.find('input.reemplazar').is(':checked');
    var opcionados = container.find('input.opcionados').is(':checked');
    var todos = container.find('input.todos').is(':checked');
    var numUsuarios = container.find('input.nUsuarios').val();

    configuracion={
                reemplazar: reemplazar,
                todos: todos,
                numUsuarios:numUsuarios
            }

    response={
                sugerir_productos: sugerir_productos,
                configuracion:configuracion


            }

    var formJson = response;
    var stringPago = JSON.stringify(formJson);
    var form = $('form#form-sugerir-producto');
    var inputJson = form.find('input#json-form-sugerir');
    inputJson.val(stringPago);
    form.submit();
});
