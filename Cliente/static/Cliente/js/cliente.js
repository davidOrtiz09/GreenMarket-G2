var URLDomain = document.location.origin+"/";

function agregarFavorito(idProducto){

    jsonFavorito = {"idProducto":idProducto};
    $.ajax({
        url: URLDomain + "favoritos",
        data: JSON.stringify(jsonFavorito),
        type: 'POST',
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function (data) {
            if(data.Mensaje === "OK")
                $("#favpro_" + idProducto).toggleClass('fa-star-o fa-star');
        },
        failure: function (errMsg) {
                    alert('Se presentó un error. No se pudo agregar favorito.');
                }
    });
}

function eliminarFavorito(idProducto){

    jsonFavorito = {"idProducto":idProducto};
    $.ajax({
        url: URLDomain + "favoritos",
        data: JSON.stringify(jsonFavorito),
        type: 'DELETE',
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function (data) {
            if(data.Mensaje === "OK")
                $("#favpro_" + idProducto).toggleClass('fa-star fa-star-o');
        },
        failure: function (errMsg) {
                    alert('Se presentó un error. No se pudo eliminar favorito.');
                }
    });
}
