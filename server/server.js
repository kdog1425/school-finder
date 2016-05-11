var express = require("express");
var bodyParser = require("body-parser");
var mongoose = require("mongoose");
var path = require("path");

//controllers
var schoolController = require("./controllers/schoolController");

//Express request pipeline
var app = express();
app.use(express.static(path.join(__dirname, "../app/dist")));
app.use(bodyParser.json())
app.use("/api", schoolController);

var port = process.env.PORT || 12810;
app.listen(port, function () {
    console.log("Started listening on port", port);
});

// Connect to mongodb database
var debug = false;
var mongodb_uri = debug ? "mongodb://localhost/schoolfinder" : process.env.MONGODB_URI;
mongoose.connect(mongodb_uri);
