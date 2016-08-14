var React = require("react");
var Center = require("react-center");
var actions = require("../actions/TrackActions");
var FileInput = require("react-file-input");
var services = require("../services/TrackAPI");
var Dropzone = require('react-dropzone');


var tracks = [];
var socket = io();

var TrackInputForm = React.createClass({
    getInitialState: function(){
      return {tracks: []};
    },
    
    onDrop: function (files) {
      console.log('Received files: ', files);
      services.uploadAudio(files);
    },

    componentDidMount: function() {
      var that = this;
      socket.on('logentry',function(log_entry){
          console.log('io message:', log_entry);
          tracks = log_entry.split(',');
          that.setState({tracks: tracks});
      });
    },

    render: function () {
      return (
        <div>
          <Center>
                <Dropzone onDrop={this.onDrop} className="audio-input-form">
                  <div>Drop a file here, or click to select a file to upload.</div>
                </Dropzone>
          </Center>
          <Center>
              <div>
                <ul className="custom-counter">
                  {this.state.tracks.map(function(listValue){
                    return <li className="results-track">{listValue}</li>;
                  })}
                </ul>
              </div>
          </Center>
        </div>
      );
    }
});

module.exports = TrackInputForm;