$(document).ready(function(){
    setShoppingCartListeners();
});

function setShoppingCartListeners(){
    $('.product-minus').click(function(){
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        if(value > 0){
            input.val(value-1);
            input.change();
        }
    });

    $('.product-plus').click(function(){
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        input.val(value+1);
        input.change();
    });

    $('input.product-quantity').change(function(){
        var value = $(this).val();
        var minus = $(this).parent().find('.product-minus');
        var addToCart = $(this).parent().parent().find('.add-to-cart');
        if(value > 0){
            addToCart.attr('disabled', false);
            minus.attr('disabled', false);
        }
        else{
            addToCart.attr('disabled', true);
            minus.attr('disabled', true);
        }
    });
}