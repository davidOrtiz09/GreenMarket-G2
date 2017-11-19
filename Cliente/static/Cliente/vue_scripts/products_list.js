var listaProductos = new Vue({
    el: '#lista-productos',
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
        incrementarCantidadCarrito: function(producto){
            producto.cantidad_carrito += 1;
        },
        disminuirCantidadCarrito: function(producto){
            var cantidadPrevia = producto.cantidad_carrito;
            if(cantidadPrevia > 0){
                producto.cantidad_carrito -= 1;
            }
        },
        cambioCantidadCarrito: function(event){
            var value = event.target.value;
            if(value < 0 || value === ''){
                event.target.value = 0;
            }
        }
    }
});