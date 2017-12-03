var URLDomain = document.location.origin+"/";
function config(){
    if($.trim( $('#mensajePython').html() ).length > 0){
        alert($.trim( $('#mensajePython').html() ));
    }
    var valueSelect = $.trim( $('#valueSelectCoop').html() );
    if($.trim( $('#valueSelectCoop').html() ).length > 0){
        $('#cooperativa').val(valueSelect);
    }
    if($.trim( $('#valueGeoLocation').html() ) == "1"){
        geoFindMe();
    }

}
$( document ).ready(function() {
  config();
});

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

    $.ajax({
        url: URLDomain+"get-cooperativa-by-location/",
        data: JSON.stringify({"longitud":longitude,"latitud":latitude}),
        type: 'POST',
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function (data) {
            console.log("Response",data);
            $('#cooperativa').val(data.idCooperativa);
            $('#botonFiltrarProductos').click();
        }
    });

}

//Función que se ejecuta en caso que no se pueda obtener la ubicación del usuario.
function errorGeolocation() {
    alert('No se puede obtener la ubicación del usuario, se recomienda permitir a la aplicación el uso de la ubicación para mejorar la interacción con el market place.');
}
