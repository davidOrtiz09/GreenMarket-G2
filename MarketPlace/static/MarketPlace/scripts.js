$(document).ready(function(){
    setAddToCartListeners();
    addCartDetailsListeners();
});

/*
    Añadimos los listeners para las funcionalidades Javascript de los detalles del carrito de compras
 */
function addCartDetailsListeners(){
    actualizarTotalPagar();
    /*
        Cuando la cantidad de un item del carrito compra cambia, se actualia el subtotal y el total de la compra
     */
    $('input.product-quantity.cart-details').change(function(){
        var quantity = $(this).val();
        if(quantity < 1){
            $(this).val(1);
        }
        else{
            var row = $(this).parent().parent().parent();
            var unitPrice = row.find('input.unit-price').val();
            var subtotal = row.find('span.subtotal-producto');
            subtotal.html(toCop(quantity*unitPrice));
            actualizarTotalPagar();
        }
    });
    
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
        var stringPago=JSON.stringify(formJson)
        var form=$('form#form-ckeckout');
        var inputJson=form.find('input#json-form');
        inputJson.val(stringPago);
        form.submit();
    });

    $(document).ready(function(){
        $("#myModal").modal('show');
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

// Listeners para la funcionalidad de añadir un producto al carrito de compras
function setAddToCartListeners() {
    // Listener para los botones de disminuir la cantidad de un producto, antes de añadirlo al carrito
    $('.product-minus').click(function () {
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        var minValue = 0;

        if(input.hasClass('cart-details')){
            minValue=1;
        }

        if (value > minValue) {
            input.val(value - 1);
            input.change();
        }
    });

    // Listener para los botones de aumentar la cantidad de un producto, antes de añadirlo al carrito
    $('.product-plus').click(function () {
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        input.val(value + 1);
        input.change();
    });

    // Listener para el input de la cantidad del producto a añadir al carrito
    $('input.product-quantity').change(function(){
        var value = $(this).val();
        var minus = $(this).parent().find('.product-minus');
        var addToCart = $(this).parent().parent().find('.add-to-cart');

        var minValue = 0;

        if($(this).hasClass('cart-details')){
            minValue = 1;
        }

        if(value > minValue){
            // Si la cantidad es mayor a 0 se habilita el botón de disminuir y el botón de de añadir al carrito
            addToCart.attr('disabled', false);
            minus.attr('disabled', false);
        }
        else{
            // Si la cantidad es menor o igual a 0 se deshabilitan los botones de disminuir cantidad y añadir al carrito
            addToCart.attr('disabled', true);
            minus.attr('disabled', true);
        }
    });
}

/*
    Se formatea un número a moneda para que sea más legible
 */
function toCop(number){
    return number.toLocaleString('en-us', {minimumFractionDigits: 0 });
}

/*
    Se actualiza el total a pagar según los items y cantidades del carrito de compras
 */
function actualizarTotalPagar(){
    var detallesPedido = $('div#detalles-pedido');
    var spanTotalPagar = detallesPedido.find('span#total-a-pagar');
    var productRows = detallesPedido.find('tr.product-cart');
    var totalPagar = 0;
    for(var i=0;i < productRows.length;i++){
        var row = $(productRows[i]);
        var unitPrice = row.find('input.unit-price').val();
        console.log(row.find('input.unit-price').val())
        var quantity = row.find('input.product-quantity.cart-details').val();
        totalPagar += (unitPrice*quantity)
    }
    spanTotalPagar.html(toCop(totalPagar));
}