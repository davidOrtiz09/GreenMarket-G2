var URLDomain = document.location.origin+"/";

function verDetalles(){
    console.log('Seguna variable:',información);
}


$('.cerrarPopUpDetalleProducto').click(function(){
    var id = $(this).attr('name');
    $("#sectionPopUpDescripcion"+id).toggle();
});

function verDetalleCarrito(id){
    $("#sectionPopUpDescripcion"+id).toggle();
}

function clicFavorito(idProducto) {
console.log('favorito' + idProducto);

    if($("#favpro_" + idProducto).is('.fa-star'))
        eliminarFavorito(idProducto);
    else
        agregarFavorito(idProducto);

}
function agregarFavorito(idProducto){

    jsonFavorito = {"idProducto":idProducto};
    $.ajax({
        url: URLDomain + "favoritos",
        data: JSON.stringify(jsonFavorito),
        type: 'POST',
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function (data) {
            console.log(data);
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
            console.log(data);
            if(data.Mensaje === "OK")
                $("#favpro_" + idProducto).toggleClass('fa-star fa-star-o');
        },
        failure: function (errMsg) {
                    alert('Se presentó un error. No se pudo eliminar favorito.');
                }
    });
}
