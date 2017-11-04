
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
