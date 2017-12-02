var map = null, marker, latSelect, longSelect;
var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
var JsonProductor = {};
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
    var correo = $("#inputCorreo").val().trim();
    var direccion = $("#inputDireccion").val().trim();
    var descripcion = $("#inputDescripcionProductor").val().trim();
    var password1 = $("#inputPassword1").val().trim();
    var password2 = $("#inputPassword2").val().trim();
    var coordenadas;


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
        alert ("Es necesario ingresar el/los nombre del productor.");
        return;
    }

    if (correo=="") {
        alert ("Es necesario ingresar el correo del productor.");
        return;
    }

    if(!pattern.test(correo)){
        alert ("Por favor ingresar un correo válido.");
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

    if (password1=="" || password2=="") {
        alert ("Es necesario ingresar dos veces la contraseña del productor.");
        return;
    }

    if (password1 != password2) {
        alert ("Las contraseñas no coinciden.");
        return;
    }


    $("#sectionLoading").show();

    JsonProductor = {"cooperativaId":cooperativaSelect.val(),"nombre":nombre,"contrasena":password1,"correo":correo,"direccion":direccion, "descripcion":descripcion, "coordenadas":coordenadas};

    $.ajax({
            url: URLDomain+"administrador/agregarProductor/",
            data: JSON.stringify(JsonProductor),
            type: 'POST',
            contentType: "application/json; charset=utf-8;",
            dataType: "json",
            success: function (data) {
                $("#sectionLoading").hide();
                alert("El productor ha sido creado de forma satisfactoria.");
                window.location = URLDomain+"administrador/productores"
            }
        });
}

function ActualizarProductor( id ){
    var nombre = $("#inputNombreActualizar").val().trim();
    var direccion = $("#inputDireccionActualizar").val().trim();
    var descripcion = $("#inputDescripcionProductorActualizar").val().trim();
    var coordenadas;

    if (nombre=="") {
        alert ("Es necesario ingresar el/los nombre del productor.");
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


    $("#sectionLoading").show();

    JsonProductor = {"nombre":nombre,"direccion":direccion, "descripcion":descripcion, "coordenadas":coordenadas, "idProductor":id};

    $.ajax({
            url: URLDomain+"administrador/actualizarProductor/",
            data: JSON.stringify(JsonProductor),
            type: 'POST',
            contentType: "application/json; charset=utf-8;",
            dataType: "json",
            success: function (data) {
                $("#sectionLoading").hide();
                alert("El productor ha sido actualizado de forma satisfactoria.");
                window.location = URLDomain+"administrador/productores"
            }
        });
}


function deleteProductor(id){
    $("#sectionLoading").show();
    $.ajax({
            url: URLDomain+"administrador/eliminarProductor/",
            data: JSON.stringify({"productorId":id}),
            type: 'POST',
            contentType: "application/json; charset=utf-8;",
            dataType: "json",
            success: function (data) {
                $("#sectionLoading").hide();
                alert("El productor ha sido eliminado de forma satisfactoria.");
                window.location = URLDomain+"administrador/productores"
            }
        });
}