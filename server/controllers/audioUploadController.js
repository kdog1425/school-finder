var _ = require("underscore");
var multer = require('multer');
var uploadRouter = require("express").Router();
var crypto = require('crypto');
var mime = require('mime');
var PythonShell = require('python-shell');

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'server/FeatureExtraction/data/uploads/')
  },
  filename: function (req, file, cb) {
    console.log("Storing...");
    crypto.pseudoRandomBytes(16, function (err, raw) {
      //cb(null, raw.toString('hex') + Date.now() + '.' + mime.extension(file.mimetype));
      cb(null, raw.toString('hex') + Date.now() + '.' + 'wav');
    });
  }
});

var uploading = multer({
  storage: storage,
  limits: {fileSize: 20000000, files:1},
});

uploadRouter.post('/audio/upload', uploading.single('audio-file'), function(req, res) {
    console.log('sessionId', req.sessionID);
    console.log('body', req.body); // form fields
    console.log('file', req.file); // form files
    var rankedList = processFile(req.file.path, req.session.id);
    res.status(204).end()
});

function processFile(path, sessionID){
    var options = {
      mode: 'text',
      pythonOptions: ['-u'],
      scriptPath: '../FeatureExtraction/main',
      args: [path]
    };
     
    pyshell = new PythonShell('go.py', options);
    pyshell.on('message', function (message) {
      // received a message sent from the Python script (a simple "print" statement)
      console.log('python: ', message);
      var substr = 'finalList&&&';
      var ranking;
      var idx = message.indexOf(substr);
      if (idx != -1){
        var messageCleaned = message.substring(idx+substr.length);  
        rankedList = JSON.parse(messageCleaned);
        console.log(rankedList);
        io.emit('logentry', rankedList.toString());
        console.log('clients: ', io.clients);
        if (clients[sessionID] == null ){
          console.log('sessionID', sessionID, ' not found!');
        } else {
          clients[sessionID].send('logentry', rankedList.toString());
        }
        return rankedList;
      }
    });
}

module.exports = uploadRouter
