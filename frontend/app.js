const express = require('express');
const path = require('path');
const logger = require('morgan');
const cors = require('cors');

// Import all the express routes we will be using
const indexRouter = require('./routes/index');

// Create our app
const app = express();

// Allows us to make requests from POSTMAN
app.use(cors());

// Set up the app to use dev logger
app.use(logger('dev'));

// Accept json
app.use(express.json());

// https://stackoverflow.com/questions/29960764/what-does-extended-mean-in-express-4-0
// Allows object nesting in POST
app.use(express.urlencoded({ extended: false }));

// Server html+css+js frontend
app.use(express.static(path.join(__dirname, 'public')));

// Connect url hierarchies to our routers
app.use('/', indexRouter);

// Catch all other routes into a meaningful error message
app.all('*', (req, res) => {
  const errorMessage = `
    Cannot find the resource <b>${req.url}</b>
  `;
  res.status(404).send(errorMessage);
});

module.exports = app;