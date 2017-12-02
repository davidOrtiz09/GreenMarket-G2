var listaCanastasApp = new Vue({
    el: '#lista-canastas-app',
    delimiters: ['[[', ']]'],
    data: {
        canastas: canastas,
    },
    mounted: function () {

    },
    computed: {
        esta_autenticado: function(){
            return autenticado;
        }
    },
    methods: {
        agregarAlCarrito: function(canasta){
            if(!this.esta_autenticado){
                alert("Para agregar canastas al carrito debes ingresar a tu cuenta");
            }
            else{
                $.ajax({
                    url: urlAgregarCanastaCarrito,
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
        }
    }
});