var cartDetailsApp = new Vue({
    el: '#cart-details-app',
    delimiters: ['[[', ']]'],
    data: {
        cart: cart,
    },
    methods: {
        toCop: function (number) {
            return number.toLocaleString('en-us', {minimumFractionDigits: 0});
        },
        getTotal: function () {
            var items = this.cart.items;
            var total = 0;
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                total += item.price * parseInt(item.quantity);
            }
            return this.toCop(total);
        },
        incrementarCantidad: function (item) {
            item.quantity += 1;
            this.modificarCantidadCarrito(item, 1);
        },
        disminuirCantidad: function (item) {
            var cantidadPrevia = parseInt(item.quantity);
            if (cantidadPrevia > 0) {
                item.quantity -= 1;
                this.modificarCantidadCarrito(item, -1);
            }
        },
        cambioCantidad: function (event, item) {
            var newValue = event.target.value;
            var previousQuantity = item.quantity;
            if (newValue < 1 || newValue === '') {
                item.quantity = 1;
            }
            else{
                item.quantity = newValue;
            }
            var diff = item.quantity - previousQuantity;
            if(diff !== 0){
                this.modificarCantidadCarrito(item, diff);
            }
        },
        modificarCantidadCarrito: function (item, quantity) {
            $.ajax({
                url: urlAgregarAlCarrito,
                type: 'POST',
                data: JSON.stringify({
                    product_id: item.product_id,
                    quantity: quantity
                }),
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                dataType: 'json',
                success: function (newCart) {
                    cartPreviewApp.updateCart(newCart);
                    cartDetailsApp.cart = newCart;
                }
            });
        },
        eliminarItem: function (item) {
            $.ajax({
                url: urlEliminarDelCarrito,
                type: 'POST',
                data: JSON.stringify({
                    product_id: item.product_id
                }),
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                dataType: 'json',
                success: function (newCart) {
                    cartPreviewApp.updateCart(newCart);
                    cartDetailsApp.cart = newCart;
                    $('#modal-eliminar-carrito-' + item.product_id).modal('hide');
                    if (cartPreviewApp.countItems() === 0) {
                        window.location.href = '/';
                    }
                }
            });
        }
    }
});