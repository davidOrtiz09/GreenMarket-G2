var cartPreviewApp = new Vue({
    el: '#cart-preview-app',
    delimiters: ['[[', ']]'],
    data: {
        cartPreview: cart,
    },
    methods: {
        countItems: function(){
            var items = this.cartPreview.items;
            var canastas = this.cartPreview.canastas;
            var response = 0;
            for(var i=0;i<items.length;i++){
                response += parseInt(items[i].quantity);
            }
            for(var i=0;i<canastas.length; i++){
                response += parseInt(canastas[i].quantity);
            }
            return response;
        },
        updateCart: function(newCart){
            this.cartPreview = newCart;
        }
    }
});