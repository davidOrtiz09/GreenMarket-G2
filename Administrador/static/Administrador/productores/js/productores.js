var map = null, marker, latSelect, longSelect;
var JsonProductor = [];
var URLDomain = document.location.origin+"/";

function iniciarMapa() {
    map = new google.maps.Map(document.getElementById('mapa'), {
        center: {lat: 4.543, lng: -74.064},
        zoom: 4
    });

    google.maps.event.addListener(map, "click", function(event) {
        latSelect = event.latLng.lat();
        longSelect = event.latLng.lng();

        placeMarker(event.latLng);
    });

    google.maps.event.trigger(map, 'resize')
}

function placeMarker(location) {
    if (marker)
    {
        marker.setMap(null)
    }
    marker = new google.maps.Marker({
        position: location,
        map: map
    });
}

$('#cerrarPopUpDetalleProducto').click(function(){
    $("#sectionMapa").toggle();
});

function verMapa(){
    $("#sectionMapa").toggle();
    if (!map){
        iniciarMapa();
    }
}

function seleccionarUbicacion(){
    if(latSelect || longSelect){
        $("#coordenadasMapa").text(latSelect.toString().substring(0,6)+","+longSelect.toString().substring(0,6));
        $("#sectionMapa").toggle();
    }
    else{
        alert("Por favor haga clic en el mapa para seleccionar una ubicación.");
    }
}

(function(){
    $.getJSON(URLDomain+"administrador/getDepartamentos/").done(function (data) {
        $("#selectDepartamento").prepend('<option disabled selected value="">Seleccione un departamento</option>');
        $.each(data.ListaDepartamentos,function (i,item) {
            $("#selectDepartamento").append('<option value="'+item.departamento+'">'+item.departamento+'</option>')
        })
    })
})();

$('#selectDepartamento').on('change', function (e) {
    $("#sectionLoading").show();
    var valueSelected = this.value;
    $("#selectCiudad").html('<option disabled selected value="">Seleccione una Ciudad</option>');
    $.getJSON(URLDomain+"administrador/getCiudadPorDepto/?idDepto="+valueSelected+"").done(function (data) {
        $.each(data.ListaCiudades,function (i,item) {
            $("#selectCiudad").append('<option value="'+item.ciudad+'" >'+item.ciudad+'</option>')
        })
        $("#sectionLoading").hide();
    })
});

$('#selectCiudad').on('change', function (e) {
    $("#sectionLoading").show();
    var valueSelected = this.value;
    $("#selectCooperativa").html('<option disabled selected value="">Seleccione una Cooperativa</option>');
    $.getJSON(URLDomain+"administrador/getCooperativaPorCiudad/?ciudad="+valueSelected+"").done(function (data) {
        $.each(data.ListaCooperativas,function (i,item) {
            $("#selectCooperativa").append('<option value="'+item.id+'" >'+item.nombre+'</option>')
        })
        $("#sectionLoading").hide();
    })
});

function agregarProductor(){
    var departamentoSelect = $("option:selected", $("#selectDepartamento"));
    var ciudadSelect = $("option:selected", $("#selectCiudad"));
    var cooperativaSelect = $("option:selected", $("#selectCooperativa"));
    var nombre = $("#inputNombre").val().trim();
    var direccion = $("#inputDireccion").val().trim();
    var descripcion = $("#inputDescripcionProductor").val().trim();
    var coordenadas;


    var unidad = $("#campoUnidad").html();


    if (typeof departamentoSelect.val() === "undefined"  || departamentoSelect.val() == ""){
        alert ("Es necesario seleccionar uno de los departamentos de la lista.");
        return;
    }

    if (typeof ciudadSelect.val() === "undefined" || ciudadSelect.val() == "" ){
        alert ("Es necesario seleccionar una ciudad de la lista.");
        return;
    }

    if (typeof cooperativaSelect.val() === "undefined" || cooperativaSelect.val() == "" ){
        alert ("Es necesario seleccionar una cooperativa de la lista.");
        return;
    }

    if (nombre=="") {
        alert ("Es necesario ingresar el nombre del productor.");
        return;
    }

    if (direccion=="") {
        alert ("Es necesario ingresar la dirección del productor.");
        return;
    }

    if (descripcion=="") {
        alert ("Es necesario ingresar una descripción del productor.");
        return;
    }

    if(latSelect || longSelect){
        coordenadas = latSelect+","+longSelect;
    }else{
        alert ("Es necesario seleccionar la ubicación de la finca del productor.");
        return;
    }





    //JsonProductor.push({"idProducto":productoSelect.val(),"Producto":productoSelect.html(),"Precio":precio,"TotalProductos":cantidad,"Unidad":unidad, "CategoriaId":categoriaSelect.val()});

    /*$.ajax({
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
        });*/
}