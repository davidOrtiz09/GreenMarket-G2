$(document).ready(function(){
    setShoppingCartListeners();
});

function setShoppingCartListeners(){
    $('.product-minus').click(function(){
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        if(value > 0){
            input.val(value-1);
        }
    });

    $('.product-plus').click(function(){
        var input = $(this).parent().parent().find('input.product-quantity');
        var value = parseInt(input.val());
        input.val(value+1);
    });

    $('.product-add').click(function(){
        $('#modal-producto-agregado').modal('show')
    });
}