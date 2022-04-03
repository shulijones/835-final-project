const express = require('express');

// const Shorts = require('../models/Shorts');

const router = express.Router();

/**
 * Serves homepage.
 * 
 * @name GET /
 */
router.get('/', (req, res) => {
  res.render('index');
});

// /**
//  * Access short URL.
//  * 
//  * @name GET /:name
//  */
// router.get('/:name?', (req, res) => {
//   // TODO implement
//   res.status(501).end();
// });

module.exports = router;