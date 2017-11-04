var JsonProductos = [];
// var URLDomain = "http://localhost:8000/";
var URLDomain = document.location.origin+"/";
renderTable();

$('#agregarProducto').click(function(){
    limpiarPopUp();
    $('#sectionAgregarProducto').toggle();
});


$('#cerrarPopUpAgregarProducto').click(function(){
    $('#sectionAgregarProducto').toggle();
});


(function(){
    $.getJSON(URLDomain+"productor/getCategorias/").done(function (data) {
        $("#selectCategoria").prepend('<option disabled selected value="">Seleccione una categoria</option>');
        $.each(data.ListaCategorias,function (i,item) {
            $("#selectCategoria").append('<option value="'+item.id+'">'+item.nombre+'</option>')
        })
    })
})();

$('#selectCategoria').on('change', function (e) {
    $("#sectionLoading").show();
    var valueSelected = this.value;
    $("#selectProductos").html('<option disabled selected value="">Seleccione un producto</option>');
    $.getJSON(URLDomain+"productor/getProductosPorCategoria/?idCategoria="+valueSelected+"").done(function (data) {
        $.each(data.ListaProductos,function (i,item) {
            $("#selectProductos").append('<option value="'+item.id+'" name="'+item.unidad_medida+'" >'+item.nombre+'</option>')
        })
        $("#sectionLoading").hide();
    })
});

$('#selectProductos').on('change', function (e) {
    var unidad = $("option:selected", this).attr('name');
    $('#campoUnidad').html(unidad);
});


function renderTable(){
    var cont = 0;
    $("#listaProductos").html('');
    $.each(JsonProductos,function (i,item) {
        $("#listaProductos").append('<tr id="'+item.idProducto+'"> <td>'+item.Producto+'</td> <td>'+item.Precio+' $ /'+item.Unidad+
            '</td> <td>'+item.TotalProductos+'</td> <td><button type="button" class="btn btn-info botonTabla" ' +
            'onclick="PopUpEditarProducto('+item.CategoriaId+', \''+item.Producto+'\', '+item.TotalProductos+', ' +
            +item.Precio+', \''+item.Unidad+'\', '+cont+');" style="">Editar</button> ' +
            '<button type="button" class="btn btn-danger botonTabla" onclick="deleteProducto('+cont+')">Eliminar</button></td> </tr>');
        cont++;
    })
}

function agregarProducto(){
    var categoriaSelect = $("option:selected", $("#selectCategoria"));
    var productoSelect = $("option:selected", $("#selectProductos"));
    var cantidad = $("#cantidadProductoOfertar").val();
    var precio = $("#precioProductoOfertar").val();
    var unidad = $("#campoUnidad").html();

    var test = categoriaSelect.val();

    if (typeof categoriaSelect.val() === "undefined"  || categoriaSelect.val() == ""){
        alert ("Es necesario seleccionar una categoria de la lista.");
        return;
    }

    if (typeof productoSelect.val() === "undefined" || productoSelect.val() == "" ){
        alert ("Es necesario seleccionar un producto de la lista.");
        return;
    }

    if (cantidad=="" || isNaN(cantidad) || cantidad <= 0 ) {
        alert ("La cantidad del producto a ofertar no puede estar vacia y debe ser un número mayor a cero.");
        return;
    }

    if (precio == "" || isNaN(precio) || precio <= 0 ) {
        alert ("El precio del producto a ofertar no puede estar vacio y debe ser un número mayor a cero.");
        return;
    }

    JsonProductos.push({"idProducto":productoSelect.val(),"Producto":productoSelect.html(),"Precio":precio,"TotalProductos":cantidad,"Unidad":unidad, "CategoriaId":categoriaSelect.val()});
    renderTable();
    $('#sectionAgregarProducto').toggle();
}

function deleteProducto(index){
    JsonProductos.splice(index, 1);
    renderTable();
}

function limpiarPopUp(){
    $("#selectCategoria").attr("disabled", false);
    $("#selectProductos").attr("disabled", false);
    $("#botonEditarProducto").hide();
    $("#botonAgregarProducto").show();
    $("#selectCategoria")[0].selectedIndex = 0;
    $("#selectProductos").html("");
    $("#cantidadProductoOfertar").val("");
    $("#precioProductoOfertar").val("");
    $("#campoUnidad").html("Unidad");
}

function PopUpEditarProducto(idCategoria, producto, cantidad, precio, unidad, posicion){
    $("#botonEditarProducto").show();
    $("#botonEditarProducto").attr("onclick", "editarProducto("+posicion+");");
    $("#botonAgregarProducto").hide();
    $("#selectCategoria").val(idCategoria);
    $("#selectCategoria").attr("disabled", true);
    $("#selectProductos").html('<option>'+producto+'</option>');
    $("#selectProductos").attr("disabled", true);
    $("#cantidadProductoOfertar").val(cantidad);
    $("#precioProductoOfertar").val(precio);
    $("#campoUnidad").html(unidad);
    $('#sectionAgregarProducto').toggle();
}

function editarProducto(posicion){

    var cantidad = $("#cantidadProductoOfertar").val();
    var precio = $("#precioProductoOfertar").val();

    if (cantidad=="" || isNaN(cantidad) || cantidad <= 0 ) {
        alert ("La cantidad del producto a ofertar no puede estar vacia y debe ser un número mayor a cero.");
        return;
    }

    if (precio == "" || isNaN(precio) || precio <= 0 ) {
        alert ("El precio del producto a ofertar no puede estar vacio y debe ser un número mayor a cero.");
        return;
    }
    JsonProductos[posicion].TotalProductos = cantidad;
    JsonProductos[posicion].Precio = precio;
    renderTable();
    $('#sectionAgregarProducto').toggle();
}

function realizarOferta(){
    $("#sectionLoading").show();
    if (JsonProductos.length == 0){
        $("#sectionLoading").hide();
        alert("Es necesario que al menos exista un producto en la oferta.");
        return;
    }

    $.ajax({
            url: URLDomain+"productor/agregarOfertaProductor/",
            data: JSON.stringify(JsonProductos),
            type: 'POST',
            contentType: "application/json; charset=utf-8;",
            dataType: "json",
            success: function (data) {
                $("#sectionLoading").hide();
                alert("La oferta ha sido creada de forma satisfactoria, el administrador revisará la solicitud.");
                window.location = URLDomain+"productor/crear-oferta"
            }
        });
}