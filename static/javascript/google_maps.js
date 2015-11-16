function initBigMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    scrollwheel: false,
    draggable: false,
    center: {lat: 0, lng: 0},
    disableDefaultUI: true,
    zoom: 14
  });

  // Bind geocoder to search bar
  var geocoder = new google.maps.Geocoder();

  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map);
  });

  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      map.setCenter(pos);
    });
  } else {
    // Browser doesn't support Geolocation
  }
}

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      resultsMap.setCenter(results[0].geometry.location);

      var result = results[0];

      var component = results[0].address_components.filter(function(item) {
        return item.types[0] === 'postal_code';
      });


      if (component.length != 0) {
        var postal_code = component[0].long_name;

        var bounds = new google.maps.LatLngBounds(
          result.geometry.viewport.getSouthWest(), 
          result.geometry.viewport.getNorthEast()
        );

        // Display bounds around the geocoded area
        displayBounds(bounds, resultsMap);

        // Display next phase alert
        // Link to /area/<zip>
        var link = "<a class=\"alert-link\" href=\"/area/" + postal_code + "\">Find out about food.</a>";
        document.getElementById("floating-alert").innerHTML = link;
        $("#floating-alert").fadeIn();

      }
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

function initRestaurantMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    // scrollwheel: false,
    // draggable: false,
    center: {lat: 0, lng: 0},
    disableDefaultUI: true,
    zoom: 14
  });

  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({'address': zip}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      map.fitBounds(results[0].geometry.viewport);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });

  restaurants.forEach(function(location) {
    var position_options = {
      lat: location.latitude,
      lng: location.longitude
    };

    var marker = new google.maps.Marker({
      position: position_options,
      map: map
    });
  })
}