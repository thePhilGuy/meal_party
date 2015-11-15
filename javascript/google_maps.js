function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    scrollwheel: false,
    center: {lat: 0, lng: 0},
    disableDefaultUI: true,
    zoom: 14
  });

  // Bind geocoder to search bar
  var geocoder = new google.maps.Geocoder();

  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map);
  });

  var infoWindow = new google.maps.InfoWindow({map: map});

  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      infoWindow.setPosition(pos);
      infoWindow.setContent('Location found.');
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });

      // Display bounds around the geocoded area
      displayBounds(results[0].geometry.bounds, resultsMap);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

function displayBounds(bounds, resultsMap) {
  // Have a global rectangle that gets moved
    var rectangleOptions = {
        strokeColor: '#0000ff',
        strokeOpacity: 0.5,
        strokeWeight: 3,
        bounds: bounds
    }
    var rectangle = new google.maps.Rectangle(rectangleOptions);
    rectangle.setMap(resultsMap);
}