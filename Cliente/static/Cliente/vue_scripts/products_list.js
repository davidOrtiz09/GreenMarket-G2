var listaProductosApp = new Vue({
    el: '#lista-productos-app',
    delimiters: ['[[', ']]'],
    data: {
        productos: productos,
        productosFiltrados: []
    },
    mounted: function () {
        this.productosFiltrados = this.productos;
    },
    methods: {
        verDetalleCarrito: function (producto) {
            $("#sectionPopUpDescripcion" + producto.id).toggle();
        },
        incrementarCantidadCarrito: function (producto) {
            producto.cantidad_carrito += 1;
        },
        disminuirCantidadCarrito: function (producto) {
            var cantidadPrevia = producto.cantidad_carrito;
            if (cantidadPrevia > 0) {
                producto.cantidad_carrito -= 1;
            }
        },
        cambioCantidadCarrito: function (event) {
            var value = event.target.value;
            if (value < 0 || value === '') {
                event.target.value = 0;
            }
        },
        agregarAlCarrito: function (producto) {
            if (autenticado) {
                $.ajax({
                    url: urlAgregarAlCarrito,
                    type: 'POST',
                    data: JSON.stringify({
                        product_id: producto.id,
                        quantity: producto.cantidad_carrito
                    }),
                    headers: {
                        'X-CSRFToken': $.cookie('csrftoken')
                    },
                    dataType: 'json',
                    success: function (newCart) {
                        producto.cantidad_carrito = 0;
                        alert("El producto fue añadido al carrito exitosamente");
                        cartPreviewApp.updateCart(newCart)
                    }
                });
            }
            else{
                alert("Para agregar productos al carrito debes autenticarte");
            }

        }
    }
});