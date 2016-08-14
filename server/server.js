var express = require("express");
var bodyParser = require("body-parser");
var path = require("path");
var morgan = require('morgan');
var cookieParser = require('cookie-parser');
var session = require('express-session')

//controllers
var audioUploadController = require("./controllers/audioUploadController");

//Express request pipeline
var app = express();
app.use(cookieParser());
app.use(session({
    secret: 'longasssecretcodehashtagpassword35', // just a long random string
    resave: false,
    saveUninitialized: true,
    key: 'express.sid'
}));

app.use(express.static(path.join(__dirname, "../app/dist")));
app.use(bodyParser.json());
app.use("/", audioUploadController);

DEBUG = false;

// log to console
app.use(morgan('dev'));
var server = require('http').createServer(app);  
io = require('socket.io')(server);

// Event fired every time a new client connects:
//----set sessionID
var cookie = require("cookie");
io.use(function(socket, next) {
  var data = socket.request;
	  //check if there's a cookie header
	    if (data.headers.cookie) {
	        // session id, as you specified in the Express setup.
	        data['sessionID'] = cookie.parse(data.headers["cookie"])["express.sid"];
	    } else {
	       // if there isn't, turn down the connection with a message
	       // and leave the function.
	       return accept('No cookie transmitted.', false);
	    }
  // make sure the handshake data looks good as before
  // if error do this:
    // next(new Error('not authorized');
  // else just call next
  next();
});

clients = {}

io.sockets.on('connection', function(socket) {
  var data = socket.handshake;
  var sessionID = cookie.parse(data.headers["cookie"])["express.sid"];
  console.log('adding sessionID', sessionID);
  var dot = sessionID.indexOf('.');
  var trimmed = sessionID.substring(2, dot);
  clients[trimmed] = socket;
  socket.join(sessionID);
});

// set the right port
var port = process.env.PORT || 12810;
if (DEBUG){
  port = 7777;
}

server.listen(port, function () {
    console.log("Started listening on port", port);
});

module.exports = io;

// app.listen(port, function () {
//     console.log("Started listening on port", port);
// });