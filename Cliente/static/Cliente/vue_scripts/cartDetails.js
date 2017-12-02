var cartDetailsApp = new Vue({
    el: '#cart-details-app',
    delimiters: ['[[', ']]'],
    data: {
        cart: cart,
        envio: {
            nombre: '',
            email: '',
            direccion: '',
            celular: '',
            telefono: '',
            observaciones: ''
        },
        pago: {
            nombre_completo: '',
            tipo_documento: 'CC',
            numero_documento: ''
        }
    },
    computed: {
        checkout_form: function () {
            var detallesPedido = this.getJsonDetallesPedido();

            var formJson = {
                detalles_pedido: detallesPedido,
                informacion_envio: this.envio,
                informacion_pago: this.pago
            };

            return JSON.stringify(formJson);
        }
    },
    methods: {
        toCop: function (number) {
            return number.toLocaleString('en-us', {minimumFractionDigits: 0});
        },
        getTotal: function () {
            var items = this.cart.items;
            var canastas = this.cart.canastas;
            var total = 0;
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                total += item.price * parseInt(item.quantity);
            }
            for(var i=0;i<canastas.length;i++){
                var canasta = canastas[i];
                total += canasta.price * parseInt(canasta.quantity);
            }
            return this.toCop(total);
        },

        incrementarCantidad: function (item) {
            var newQuantity = item.quantity + 1;
            if(newQuantity <= item.cantidad_disponible){
                item.quantity += 1;
                this.modificarCantidadCarrito(item, 1);
            }
        },
        disminuirCantidad: function (item) {
            var cantidadPrevia = parseInt(item.quantity);
            if (cantidadPrevia > 0) {
                item.quantity -= 1;
                this.modificarCantidadCarrito(item, -1);
            }
        },
        cambioCantidad: function (event, item) {
            var newValue = parseInt(event.target.value);
            var previousQuantity = item.quantity;
            if (newValue < 1 || newValue === '') {
                item.quantity = 1;
            }
            else {
                if(newValue > item.cantidad_disponible){
                    item.quantity = item.cantidad_disponible;
                }
                else{
                    item.quantity = newValue;
                }
            }
            var diff = item.quantity - previousQuantity;
            if (diff !== 0) {
                this.modificarCantidadCarrito(item, diff);
            }
        },
        modificarCantidadCarrito: function (item, quantity) {
            if(quantity > item.cantidad_disponible){
                quantity = item.cantidad_disponible - item.quantity;
            }
            if(quantity < 1){
                quantity = 1 - item.quantity;
            }

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
        },

        incrementarCantidadCanasta: function (canasta) {
            var newQuantity = canasta.quantity + 1;
            if(newQuantity <= canasta.cantidad_disponible){
                canasta.quantity += 1;
                this.modificarCantidadCanasta(canasta, 1);
            }
        },
        disminuirCantidadCanasta: function (canasta) {
            var cantidadPrevia = parseInt(canasta.quantity);
            if (cantidadPrevia > 0) {
                canasta.quantity -= 1;
                this.modificarCantidadCanasta(canasta, -1);
            }
        },
        cambioCantidadCanasta: function (event, canasta) {
            var newValue = parseInt(event.target.value);
            var previousQuantity = parseInt(canasta.quantity);
            console.log(newValue, previousQuantity);
            if (newValue < 1 || newValue === '') {
                canasta.quantity = 1;
            }
            else {
                if(newValue > canasta.cantidad_disponible){
                    canasta.quantity = canasta.cantidad_disponible;
                }
                else{
                    canasta.quantity = newValue;
                }
            }
            var diff = canasta.quantity - previousQuantity;
            if (diff !== 0) {
                this.modificarCantidadCanasta(canasta, diff);
            }
        },
        eliminarCanasta: function(canasta){
            $.ajax({
                url: urlEliminarCanastaDelCarrito,
                type: 'POST',
                data: JSON.stringify({
                    canasta_id: canasta.id
                }),
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                dataType: 'json',
                success: function (newCart) {
                    cartPreviewApp.updateCart(newCart);
                    cartDetailsApp.cart = newCart;
                    $('#modal-eliminar-canasta-' + canasta.id).modal('hide');
                    if (cartPreviewApp.countItems() === 0) {
                        window.location.href = '/';
                    }
                }
            });
        },
        modificarCantidadCanasta: function (canasta, quantity) {
            if(quantity > canasta.cantidad_disponible){
                quantity = canasta.cantidad_disponible - canasta.quantity;
            }
            if(quantity < 1){
                quantity = 1 - canasta.quantity;
            }
            $.ajax({
                url: urlAgregarCanastaAlCarrito,
                type: 'POST',
                data: JSON.stringify({
                    canasta_id: canasta.id,
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

        pagarPedido: function () {
            var form = $('form#form-ckeckout');
            this.validateForm();
            if (form.valid()) {
                form.submit();
            }
        },
        validateForm: function () {
            var form = $('form#form-ckeckout');
            form.validate({
                errorPlacement: function (error, element) {
                    var placement = $(element).data('error');
                    if (placement) {
                        $(placement).append(error)
                    } else {
                        error.insertAfter(element);
                    }
                },
                errorElement: 'div',
                errorClass: 'text-danger',
                rules: {
                    nombre: {
                        required: true
                    },
                    email: {
                        email: true
                    },
                    direccion: {
                        required: true
                    },
                    celular: {
                        required: true,
                        number: true
                    },
                    telefono: {
                        number: true
                    },
                    'nombre-completo': {
                        required: true
                    },
                    'tipo_documento': {
                        required: true
                    },
                    'numero-documento': {
                        required: true,
                        number: true
                    }
                },
                messages: {
                    nombre: {
                        required: "* Por favor ingrese su nombre"
                    },
                    email: {
                        email: "* Por favor ingrese un correo electrónico válido",
                        required: "* Por favor ingrese su correo electrónico"
                    },
                    direccion: {
                        required: '* Por favor ingrese la dirección de entrega'
                    },
                    celular: {
                        required: '* Por favor ingrese su número de celular',
                        number: '* Por favor ingrese un número de celular válido'
                    },
                    telefono: {
                        number: '* Por favor ingrese un número de teléfono válido'
                    },
                    'nombre-completo': {
                        required: '* Por favor ingrese su nombre completo'
                    },
                    'tipo-documento':{
                        required: '* Por favor seleccione un tipo de documento'
                    },
                    'numero-documento':{
                        required: '* Por favor ingrese su número de documento',
                        number: '* Por favor ingrese un número de identificación válido'
                    }
                }
            });
        },
        getJsonDetallesPedido: function () {
            var response = [];
            for (var i = 0; i < this.cart.items.length; i++) {
                var item = this.cart.items[i];
                response.push({
                    quantity: item.quantity,
                    product_id: item.product_id
                })
            }
            return response;
        }
    }
});