var express = require("express");
var bodyParser = require("body-parser");
var morgan      = require('morgan');
var mongoose = require("mongoose");
var passport	= require('passport');
var path = require("path");
var DEBUG = true;


//Express request pipeline
var app = express();
// Use the passport package in our application
app.use(passport.initialize());

// pass passport for configuration
require('../config/passport')(passport);

app.use(express.static(path.join(__dirname, "../app/dist")));
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
  extended: true
}));

//controllers
var schoolController = require("./controllers/schoolController");
var authenticationController = require("./controllers/authenticationController");
app.use("/api", schoolController);
app.use("/api", authenticationController);

// log to console
app.use(morgan('dev'));

// Connect to mongodb database
var mongodb_uri = DEBUG ? "mongodb://localhost/schoolfinder" : process.env.MONGODB_URI;
mongoose.connect(mongodb_uri);

// set the right port
var port = process.env.PORT || 12810;
if (DEBUG){
	port = 3000;
}
app.listen(port, function () {
    console.log("Started listening on port", port);
});
