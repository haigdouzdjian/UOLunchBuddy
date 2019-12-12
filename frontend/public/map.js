/* Keep the following comment at the top of the file */
/* eslint-disable no-unused-vars */
/* global fetch, mapboxgl */
mapboxgl.accessToken =
  'pk.eyJ1IjoibWhlcm5hbiIsImEiOiJjazNpdGNqOWUwYnpjM2RtdjJsd2M3cTB1In0.RFvEbY3cMo1uh_cVOvjFZQ'
var stores = {} // Stores list is empty initially

/* API calls */
const getRestaurants = async () => {
  const response = await fetch('/restaurants')
  const json = await response.json()
  stores = json
}
getRestaurants() // Get our data

/* Map */

// Add map to the page
var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10?optimize=true',
  center: [-123.074223, 44.044734],
  zoom: 14
})

// Load stores onto map
map.on('load', function (e) {
  // Add markers to map
  map.addSource('place', {
    type: 'geojson',
    data: stores
  })
  // Add marker to each store
  stores.features.forEach(function (marker, index) {
    // Marker div
    var el = document.createElement('div')
    el.className = 'marker'
    // Custom marker creation and position
    new mapboxgl.Marker(el, { offset: [0, -23] })
      .setLngLat(marker.geometry.coordinates)
      .addTo(map)

    // Event listener for when marker is clicked
    el.addEventListener('click', function (e) {
      var activeItem = document.getElementsByClassName('active')
      flyToStore(marker)
      createPopUp(marker)
      // Highlight the store in the sidebar
      e.stopPropagation()
      if (activeItem[0]) {
        activeItem[0].classList.remove('active')
      }
      var listing = document.getElementById('listing-' + index)
      listing.classList.add('active')
      //listing.scrollIntoView()
    })
  })

  // Add stores to sidebar
  buildLocationList(stores)
})

/* Sidebar */

// Read each store into our sidebar
function buildLocationList (data) {
  for (let i = 0; i < data.features.length; i++) {
    var currentFeature = data.features[i]
    var prop = currentFeature.properties // Just so we can use 'prop' as shorthand
    // Div container for every store
    var listings = document.getElementById('listings')
    var listing = listings.appendChild(document.createElement('div'))
    listing.className = 'item'
    listing.id = 'listing-' + i

    // Title link
    var link = listing.appendChild(document.createElement('a'))
    link.href = '#'
    link.className = 'title'
    link.dataPosition = i
    link.innerHTML = prop.name

    // Event listener for when title is clicked
    link.addEventListener('click', function (e) {
      var clickedListing = data.features[this.dataPosition]
      flyToStore(clickedListing)
      createPopUp(clickedListing)
      var activeItem = document.getElementsByClassName('active')
      if (activeItem[0]) {
        activeItem[0].classList.remove('active')
      }
      this.parentNode.classList.add('active')
    })

    // Listing details
    var details = listing.appendChild(document.createElement('div'))
    details.innerHTML = prop.cuisines
    details.className = 'details'
    // Location
    var listingLocation = listing.appendChild(document.createElement('div'))
    listingLocation.innerHTML += 'Location: ' + prop.location
    listingLocation.className = 'location'
    // Hours
    if (prop.hours) {
      var listingHours = listing.appendChild(document.createElement('div'))
      listingHours.innerHTML += '\nHours: ' + prop.hours
      listingHours.className = 'hours'
    }
    // Meal Plan
    var listingMealPoints = listing.appendChild(document.createElement('div'))
    listingMealPoints.className = 'meal_points'
    if (prop.meal_points) {
      listingMealPoints.innerHTML += 'Meal Plan: Yes'
    } else {
      listingMealPoints.innerHTML += 'Meal Plan: No'
    }
    // Duck Bucks
    var listingDuckBucks = listing.appendChild(document.createElement('div'))
    listingDuckBucks.className = 'duck_bux'
    if (prop.duck_bux) {
      listingDuckBucks.innerHTML += 'Duck Bucks: Yes'
    } else {
      listingDuckBucks.innerHTML += 'Duck Bucks: No'
    }
  }
}

/* Interactivity functions */

function flyToStore (currentFeature) {
  map.flyTo({
    center: currentFeature.geometry.coordinates,
    zoom: 17
  })
}

function createPopUp (currentFeature) {
  var popUps = document.getElementsByClassName('mapboxgl-popup')
  // Check if there is already a popup on the map, if so, remove it
  if (popUps[0]) popUps[0].remove()

  var popup = new mapboxgl.Popup({ closeOnClick: false })
    .setLngLat(currentFeature.geometry.coordinates)
    .setHTML(
      '<h3>' +
        currentFeature.properties.name +
        '</h3>' +
        '<h4>' +
        currentFeature.properties.location +
        '</h4>'
    )
    .addTo(map)
}

/* Keep the following comment at the bottom of the file */
/* eslint-disable no-unused-vars */
