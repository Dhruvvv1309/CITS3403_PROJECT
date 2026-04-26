function initMap() {
  const location = { lat: -31.9505, lng: 115.8605 };

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 13,
    center: location,
  });

  new google.maps.Marker({
    position: location,
    map: map,
    title: "Coffee Spots Nearby"
  });
}