let map;
let markers = [];

function initMap() {
  //Map Options
  var options = {
    zoom: 12,
    center: { lat: 40.8623889, lng: -73.8794421 },
  };

  //New map
  map = new google.maps.Map(document.getElementById("map"), options);
}


var culture = [
  //Cloister
  {
    coords: { lat: 40.8648628, lng: -73.9339214 },
    label: "A",
  },
  //Bronx Musuem of Art
  {
    coords: { lat: 40.830572, lng: -73.919326 },
    label: "B",
  },
  //Hudson River Museum
  {
    coords: { lat: 40.9555427, lng: -73.8962114 },
    label: "D",
  },
];

var activities = [
  //Bronx Botanical Garden
  {
    coords: { lat: 40.8608692, lng: -73.8827259 },
    label: "A",
  },
  //Wave Hill
  {
    coords: { lat: 40.8978503, lng: -73.9136364 },
    label: "B",
  },
  //Bronx Zoo
  {
    coords: { lat: 40.8505949, lng: -73.8769982 },
    label: "C",
  },
  //Van Cortlandt Park Golf Course
  {
    coords: { lat: 40.8889039, lng: -73.894598 },
    label: "D",
  },
  //Mosholu Golf Course
  {
    coords: { lat: 40.8893038, lng: -73.8835135 },
    label: "E",
  },
];

function actMarkers(){
    console.log("Act");
    deleteMarkers();
    setMarkers(activities);
}

function cultureMarkers(){
    deleteMarkers();
    setMarkers(culture);
}

function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }

function setMarkers(marks){
    for(let i=0;i < marks.length; i++) {
        addMarkers(marks[i]);
    }
}

function addMarkers(props) {
  const marker = new google.maps.Marker({
    position: props.coords,
    map: map,
    label: props.label,
  });
  markers.push(marker);
}

function clearMarkers() {
  setMapOnAll(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
  }