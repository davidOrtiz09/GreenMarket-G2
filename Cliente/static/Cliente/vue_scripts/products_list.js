var listaOrdenes = [
    {
        texto: 'Producto: A-Z',
        orden: 'nombre'
    },
    {
        texto: 'Producto: Z-A',
        orden: '-nombre'
    },
    {
        texto: 'Precio: Menor a mayor',
        orden: 'precio'
    },
    {
        texto: 'Precio: Mayor a menor',
        orden: '-precio'
    }
];
var listaProductosApp = new Vue({
    el: '#lista-productos-app',
    delimiters: ['[[', ']]'],
    data: {
        productos: productos,
        productosFiltrados: [],
        ordenes: listaOrdenes,
        ordenSeleccionado: listaOrdenes[0],
        soloFavoritos: false
    },
    watch: {
        soloFavoritos: function(newValue){
            this.productosFiltrados = this.productos.filter(function(producto){
                if(listaProductosApp.soloFavoritos){
                    return producto.es_favorito;
                }
                return true;
            });
            this.cambioOrden();
        }
    },
    mounted: function () {
        this.productosFiltrados = this.productos;
    },
    computed: {
        esta_autenticado: function(){
            return autenticado;
        }
    },
    methods: {
        cambioOrden: function(){
            var orden = this.ordenSeleccionado.orden;
            if(orden === 'nombre'){
                this.ordenarPorNombreAZ();
            }
            else if(orden === '-nombre'){
                this.ordenarPorNombreZA();
            }
            else if(orden === 'precio'){
                this.ordenarPorPrecioMenorMayor();
            }
            else if(orden === '-precio'){
                this.ordenarPorPrecioMayorMenor()
            }
        },
        ordenarPorNombreAZ: function(){
            this.productosFiltrados = this.productosFiltrados.sort(function(a, b){
                return a.nombre.localeCompare(b.nombre);
            });
        },
        ordenarPorNombreZA: function(){
            console.log("entra");
            this.productosFiltrados = this.productosFiltrados.sort(function(a, b){
                return b.nombre.localeCompare(a.nombre);
            });
        },
        ordenarPorPrecioMenorMayor: function(){
            this.productosFiltrados = this.productosFiltrados.sort(function(a, b){
                return a.precio > b.precio;
            });
        },
        ordenarPorPrecioMayorMenor: function(){
            this.productosFiltrados = this.productosFiltrados.sort(function(a, b){
                return a.precio < b.precio;
            });
        },
        verDetalleCarrito: function (producto) {
            $("#sectionPopUpDescripcion" + producto.id).toggle();
        },
        incrementarCantidadCarrito: function (producto) {
            var cantidadPrevia = producto.cantidad_carrito;
            if(cantidadPrevia < producto.cantidad_disponible){
                producto.cantidad_carrito += 1;
            }
            else{
                producto.cantidad_carrito = producto.cantidad_disponible;
            }

        },
        disminuirCantidadCarrito: function (producto) {
            var cantidadPrevia = producto.cantidad_carrito;
            if (cantidadPrevia > 0) {
                producto.cantidad_carrito -= 1;
            }
        },
        cambioCantidadCarrito: function (event, producto) {
            var value = event.target.value;
            if (value < 0 || value === '') {
                event.target.value = 0;
            }
            else if(value > producto.cantidad_disponible){
                event.target.value = producto.cantidad_disponible;
            }
        },
        agregarFavorito: function(producto){
            if (autenticado) {
                $.ajax({
                    url: urlAgregarFavorito,
                    type: 'POST',
                    data: JSON.stringify({
                        id_producto: producto.id_producto
                    }),
                    headers: {
                        'X-CSRFToken': $.cookie('csrftoken')
                    },
                    dataType: 'json',
                    success: function (message) {
                        producto.es_favorito = true;
                        alert("El producto fue añadido como favorito");
                    },
                    failure: function (errMsg) {
                        alert('Se presentó un error. No se pudo agregar como favorito.');
                    }
                });
            }
            else{
                alert("Para agregar favoritos debes autenticarte");
            }
        },
        eliminarFavorito: function(producto){
            if (autenticado) {
                $.ajax({
                    url: urlEliminarFavorito,
                    type: 'POST',
                    data: JSON.stringify({
                        id_producto: producto.id_producto
                    }),
                    headers: {
                        'X-CSRFToken': $.cookie('csrftoken')
                    },
                    dataType: 'json',
                    success: function (message) {
                        producto.es_favorito = false;
                        alert("El producto fue eliminado de sus favoritos");
                    },
                    failure: function (errMsg) {
                        alert('Se presentó un error. No se pudo eliminar como favorito.');
                    }
                });
            }
            else{
                alert("Para agregar favoritos debes autenticarte");
            }
        },
        agregarAlCarrito: function (producto) {
            if (autenticado) {
                $.ajax({
                    url: urlAgregarAlCarrito,
                    type: 'POST',
                    data: JSON.stringify({
                        product_id: producto.id_producto,
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