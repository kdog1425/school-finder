var React = require("react");
var ReactDOM = require("react-dom");
var Center = require('react-center');
var Router = require("react-router").Router;
var Route = require("react-router").Route;
var IndexRoute = require("react-router").IndexRoute;
var Link = require("react-router").Link;
var hashHistory = require("react-router").hashHistory;
var browserHistory = require("react-router").browserHistory;
var TrackInputForm = require("./components/TrackInputForm.jsx");
var tracksStore = require("./stores/tracksStore");
var _tracks = [];

var getTracksCallback = function(tracks){
    _tracks = tracks;
    renderTracks();
};

function renderTracks(){
    ReactDOM.render(<TracksList tracks={_tracks} />, document.getElementById("container"));
}

function initTracksView(){
	tracksStore.onChange(getTracksCallback);
}

var Layout = React.createClass({
   render:function(){
     console.log('render layout');
       return (
          <div id="layout"> 
            <div>
              {this.props.children}
            </div>
          </div>
       );
   } 
});
 
function render(){
    ReactDOM.render(
    	<Router history={browserHistory}>
	        <Route path="/" component={Layout} >
	          <IndexRoute component={TrackInputForm} />
	          <Route path="queryTrack" component={TrackInputForm} />
	        </Route>
    	</Router>, document.getElementById('container')
    );
}

render();



