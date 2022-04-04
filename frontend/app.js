const express = require('express');
const path = require('path');
// const cookieParser = require('cookie-parser');
const logger = require('morgan');
// const session = require('express-session');
const cors = require('cors');

// Import all the express routes we will be using
const indexRouter = require('./routes/index');
// const shortsRouter = require('./routes/shorts');
// const usersRouter = require('./routes/users');

// Create our app
const app = express();

// Set up user session
// app.use(session({
//   secret: 'URL-shortener',
//   resave: true,
//   saveUninitialized: true
// }));

// Allows us to make requests from POSTMAN
app.use(cors({ credentials: true, origin: [`http://localhost:5000`, `https://localhost:3000`], }));

// Set up the app to use dev logger
app.use(logger('dev'));

// Accept json
app.use(express.json());

// https://stackoverflow.com/questions/29960764/what-does-extended-mean-in-express-4-0
// Allows object nesting in POST
app.use(express.urlencoded({ extended: false }));

// Cookies for sessions
// app.use(cookieParser());

// Server html+css+js frontend
app.use(express.static(path.join(__dirname, 'public')));

// Connect url hierarchies to our routers
app.use('/', indexRouter);
// app.use('/api/shorts', shortsRouter);
// app.use('/api/session', usersRouter);

// Catch all other routes into a meaningful error message
app.all('*', (req, res) => {
  const errorMessage = `
    Cannot find the resource <b>${req.url}</b>
    <br>
    Please use only supported routes below
    <br><br>
    <b>Home Page and URL Shortening</b>
    <br>
    GET / -- Go to home page
    <br>
    GET /:name -- Go to URL of short named :name
    <br><br>
    <b>Shorts</b>
    <br>
    GET /api/shorts -- Display all shorts stored on the server
    <br>
    POST /api/shorts -- Create and store a new short on the server
    <br>
    PUT /api/shorts/:name -- Update the short on the server with short name :name
    <br>
    DELETE /api/shorts/:name -- Delete the short on the server with short name :name
    <br><br>
    <b>Authentication</b>
    <br>
    POST /api/session -- Authenticate with username into the server
  `;

  res.status(404).send(errorMessage);
});

module.exports = app;