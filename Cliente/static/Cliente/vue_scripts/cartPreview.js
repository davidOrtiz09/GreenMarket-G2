var cartPreviewApp = new Vue({
    el: '#cart-preview-app',
    delimiters: ['[[', ']]'],
    data: {
        cartPreview: cartPreview,
    },
    methods: {
        countItems: function(){
            var items = this.cartPreview.items;
            var response = 0;
            for(var i=0;i<items.length;i++){
                response += items[i].quantity;
            }
            return response;
        }
    }
});