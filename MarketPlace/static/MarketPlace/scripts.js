$(document).ready(function(){
    setAddToCartListeners();
    addCartDetailsListeners();
});

/*
    Añadimos los listeners para las funcionalidades Javascript de los detalles del carrito de compras
 */
function addCartDetailsListeners(){
    /*
        Cuando le da click en pagar, se obtienen los datos de los 3 formularios, para posteriormente hacerles post
     */
    $('button#pagar').click(function(){
        var detallesPedido = getJsonDetallesPedido();
        var informacionEnvio = getJsonInfoEnvio();
        var informacionPago = getJsonInfoPago();


        var formJson = {
            detalles_pedido: detallesPedido,
            informacion_envio: informacionEnvio,
            informacion_pago: informacionPago
        };
        var stringPago=JSON.stringify(formJson);
        var form=$('form#form-ckeckout');
        var inputJson=form.find('input#json-form');
        inputJson.val(stringPago);
        form.submit();
    });
}

/*
    Obtenemos la información de los detalles de compra
 */
function getJsonDetallesPedido(){
    var container = $('div#detalles-pedido');
    var response = [];
    var productRows = container.find('tr.product-cart');
    for(var i=0;i < productRows.length;i++){
        var row = $(productRows[i]);
        var productId = row.find('input.product-id').val();
        var quantity = row.find('input.product-quantity.cart-details').val();
        response.push({
            quantity: quantity,
            product_id: productId
        })
    }
    return response;
}

/*
    Obtenemos la información que el usuario llenó en los datos de envío
 */
function getJsonInfoEnvio(){
    var container = $('div#formulario-informacion-envio');

    var nombre = container.find('input[name="nombre"]').val();
    var email =  container.find('input[name="email"]').val();
    var direccion =  container.find('input[name="direccion"]').val();
    var celular =  container.find('input[name="celular"]').val();
    var telefono =  container.find('input[name="telefono"]').val();
    var observaciones =  container.find('textarea[name="observaciones"]').val();

    return {
        nombre: nombre,
        email: email,
        direccion: direccion,
        celular: celular,
        telefono: telefono,
        observaciones: observaciones
    }
}

/*
    Obtenemos la información que el usuario puso en el formulario de pago
 */
function getJsonInfoPago(){
    var container = $('div#formulario-informacion-pago');

    var nombreCompleto = container.find('input[name="nombre-completo"]').val();
    var tipoDocumento = container.find('select[name="tipo-documento"]').val();
    var numeroDocumento = container.find('input[name="numero-documento"]').val();

    return {
        nombre_completo: nombreCompleto,
        tipo_documento: tipoDocumento,
        numero_documento: numeroDocumento
    }
}

/*
    Se formatea un número a moneda para que sea más legible
 */
function toCop(number){
    return number.toLocaleString('en-us', {minimumFractionDigits: 0 });
}