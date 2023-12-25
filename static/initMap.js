function initMap() {
    map = new OpenLayers.Map('map');
    basemap = new OpenLayers.Layer.OSM("Simple OSM Map");
    map.addLayer(basemap);
    markers = new OpenLayers.Layer.Markers("Markers");
    map.addLayer(markers);
  }

function addMarker() {
    var input = document.getElementById("location").value.split(',');
    var latitude = parseFloat(input[0])
    var longitude = parseFloat(input[1])
    var lonLat = new OpenLayers.LonLat(longitude, latitude)
      .transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        map.getProjectionObject() // to Spherical Mercator Projection
      );
    var point = new OpenLayers.Marker(lonLat);
    markers.addMarker(point);
    map.setCenter(lonLat, 8); // second arg is zoom level
    //console.log(latitude + ", " + longitude);
}

function addMarkerCity(latitude, longitude) {
  var latitude = parseFloat(latitude);
  var longitude = parseFloat(longitude);
  var lonLat = new OpenLayers.LonLat(longitude, latitude)
    .transform(
      new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
      map.getProjectionObject() // to Spherical Mercator Projection
    );
  var point = new OpenLayers.Marker(lonLat);
  markers.addMarker(point);
  map.setCenter(lonLat, 8); // second arg is zoom level
}

// load and setup map layers
initMap();