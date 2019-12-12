const express = require('express')
const fetch = require('node-fetch')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const app = express()

// Start the server
const port = process.env.PORT
app.listen(port, () => {
  console.log(`listening at ${port}.`)
})

// Serve pages
app.use(express.static('public'))
app.use(bodyParser.json()) // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded
app.use(cookieParser())

// Calls to the API
app.get('/cuisines', async (request, response) => {
  const apiURL = 'http://localhost:3600/cuisines'
  const apiResponse = await fetch(apiURL)
  const data = await apiResponse.json()
  response.json(data.cuisines)
})

// Send preferences to API
// Get list of restaurants that meet those requirments
// Send list of retataurants to client
app.get('/restaurants', async (request, response) => {
  console.log('Cookies :  ', request.cookies.cuisine_cookie)
  const cuisineChoice = request.cookies.cuisine_cookie
  const apiURL = 'http://localhost:3600/restaurants'
  const apiResponse = await fetch(apiURL, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(cuisineChoice)
  })
  const data = await apiResponse.json()
  console.log(data)
  response.json(data.restaurants)
})

// Cookies
app.post('/cookies', (request, response) => {
  // Cookie that stores the user's lunch preference
  // the request.body is the value of the cookie
  // cookie expires after 1 minute
  response.cookie('cuisine_cookie', request.body, { maxAge: 60000 }).send('Cookie is set')
})

// Form handlers
app.get('/cuisine-form', (request, response) => {
  response.redirect('/loader.html')
})
