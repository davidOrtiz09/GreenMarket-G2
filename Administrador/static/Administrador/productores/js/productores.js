var map = null, marker, latSelect, longSelect;

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
        alert("Lo va a crear...");
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