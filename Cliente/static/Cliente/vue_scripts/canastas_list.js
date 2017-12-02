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
                        id_canasta: canasta.id,
                        quantity: 1
                    }),
                    headers: {
                        'X-CSRFToken': $.cookie('csrftoken')
                    },
                    dataType: 'json',
                    success: function (newCart) {
                        alert("La canasta se agregó al carrito")
                        cartPreviewApp.updateCart(newCart);
                    },
                    failure: function (errMsg) {
                        alert('Se presentó un error. No se pudo agregar la canasta al carrito.');
                    }
                });
            }
        }
    }
});