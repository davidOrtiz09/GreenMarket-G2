$(document).ready(function () {
    $("#fcatalogo").submit(function (event) {

        // Se obtienen todos los elementos donde se tienen los precios.
        var display = $('.precio');
        var proPre = [];
        var i;
        // Se arma el objeto JSON con los datos a enviar, id del producto con su  respectivo precio.
        for (i = 0; i < display.length; i++) {
            proPre.push({
                producto: display[i].id.split('_')[1],
                precio: display[i].value
            });
        }

        // Se actualiza el campo hidden del formulario con el dato a enviar.
        var precios_enviar = $("#precios_enviar");
        precios_enviar.val(JSON.stringify(proPre));
        return true;
        //$( "#fcatalogo" ).submit();
    });
});
