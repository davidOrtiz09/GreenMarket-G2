
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

//Función que ejecuta las funcionalidades asociadas a la ubicación del usuario y las cooperativas que corresponder a esa ubicación.
function geoFindMe() {

  if (!navigator.geolocation){
      alert('El navegador no soporta la Geolocalización, no se puede mostrar la cooperativa según su ubicación.');
      return;
  }

  navigator.geolocation.getCurrentPosition(successGeolocation, errorGeolocation);
}

//Función que es ejecutada una vez se obtiene la ubicación del usuario y la cual seleciona la cooperativa correspondiente.
function successGeolocation(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;

    $.get( "http://maps.googleapis.com/maps/api/geocode/json?latlng="+latitude+","+longitude, function( data ) {
        var ciudadFinal, ciudad, ciudadBogota;
        //Se necesitan recorrer todos los elementos del geocodificador para identificar cual es la ciudad
        for (var i=0; i<data.results[0].address_components.length; i++) {
            for (var b = 0; b < data.results[0].address_components[i].types.length; b++) {
                //El tipo area administrativa de nivel 1 es la ciudad
                if (data.results[0].address_components[i].types[b] == "administrative_area_level_2") {
                    ciudad = data.results[0].address_components[i];
                    break;
                }
                if (data.results[0].address_components[i].types[b] == "administrative_area_level_1") {
                    ciudadBogota = data.results[0].address_components[i];
                    break;
                }
            }
        }
        if(ciudad == null){
            ciudadFinal = ciudadBogota;
        }else{
            ciudadFinal = ciudad;
        }
        if(ciudadFinal != null){
            window.open(window.location.href.split("?")[0]+'?ciudadGeo='+ciudadFinal.short_name,"_self");
        }
        else{
            alert("No se pudo encontrar una ciudad en la ubicación seleccionada.")
        }
    });

}

//Función que se ejecuta en caso que no se pueda obtener la ubicación del usuario.
function errorGeolocation() {
    alert('No se puede obtener la ubicación del usuario, se recomienda permitir a la aplicación el uso de la ubicación para mejorar la interacción con el market place.');
}

//Función utilizada par obtener los parametros Get de la aplicación.
function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

function config(){
    if($.trim( $('#mensajePython').html() ).length > 0){
        alert($.trim( $('#mensajePython').html() ));
    }
    var valueSelect = $.trim( $('#valueSelectCoop').html() );
    if($.trim( $('#valueSelectCoop').html() ).length > 0){
        $('#cooperativa').val(valueSelect);
    }
}

config();