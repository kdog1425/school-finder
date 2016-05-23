var React = require("react");
var ReactDOM = require("react-dom");
var Center = require('react-center');

var SchoolsList = require("./components/SchoolsList.jsx");
var schoolsStore = require("./stores/schoolsStore");
var _schools = [];
var getSchoolsCallback = function(schools){
    _schools = schools;
    renderSchools();
};

function renderSchools(){
    ReactDOM.render(<SchoolsList schools={_schools} />, document.getElementById("container"));
}

function initSchoolsView(){
	schoolsStore.onChange(getSchoolsCallback);
}

var Login = require("./components/Login.jsx");
var loginStore = require("./stores/loginStore");
var submitLoginCredentialsCallback = function(credentials){
    _credentials = credentials;
    renderLogin();
};
loginStore.onChange(submitLoginCredentialsCallback);

function renderLogin(){
	ReactDOM.render(<Center><Login loginSuccessCallback={initSchoolsView}/></Center>, document.getElementById("container"));    
}
//renderLogin();
initSchoolsView();





