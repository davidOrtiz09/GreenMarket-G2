var cartPreviewApp = new Vue({
    el: '#cart-preview-app',
    delimiters: ['[[', ']]'],
    data: {
        cartPreview: cart,
    },
    methods: {
        countItems: function(){
            var items = this.cartPreview.items;
            var response = 0;
            for(var i=0;i<items.length;i++){
                response += parseInt(items[i].quantity);
            }
            return response;
        },
        updateCart: function(newCart){
            this.cartPreview = newCart;
        }
    }
});