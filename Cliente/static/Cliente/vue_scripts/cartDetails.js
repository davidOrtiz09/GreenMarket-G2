var cartDetailsApp = new Vue({
    el: '#cart-details-app',
    delimiters: ['[[', ']]'],
    data: {
        cart: cart,
    },
    methods: {
        toCop: function(number){
            return number.toLocaleString('en-us', {minimumFractionDigits: 0 });
        },
        getTotal: function(){
            var items = this.cart.items;
            var total = 0;
            for(var i=0;i<items.length;i++){
                var item = items[i];
                total += item.price * parseInt(item.quantity);
            }
            return this.toCop(total);
        },
        incrementarCantidad: function(item){
             item.quantity += 1;
        },
        disminuirCantidad: function(item){
            var cantidadPrevia = parseInt(item.quantity);
            if(cantidadPrevia > 0){
                item.quantity -= 1;
            }
        },
        cambioCantidad: function(event){
            var value = event.target.value;
            if(value < 1 || value === ''){
                event.target.value = 1;
            }
        }
    }
});