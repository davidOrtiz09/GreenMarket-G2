$(document).ready(function(){
    setAddToCartListeners();
});

// Listeners para la funcionalidad de añadir un producto al carrito de compras
function setAddToCartListeners() {
    // Listener para los botones de disminuir la cantidad de un producto, antes de añadirlo al carrito
    $('.product-minus').click(function () {
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        if (value > 0) {
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
        if(value > 0){
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