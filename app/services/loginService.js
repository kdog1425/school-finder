var $ = require("jquery");
var promise = require("es6-promise");
//var resourceUrl = "https://radiant-springs-58285.herokuapp.com/api/authenticate";
var resourceUrl = "http://localhost:3000/api/authenticate";

module.exports = {
    submitLoginCredentials: function (credentials) {
        var Promise = promise.Promise;
        return new Promise(function (resolve, reject) {
            $.ajax({
                url: resourceUrl,
                data: "name=" + encodeURIComponent(credentials.email) +
                     "&password=" + encodeURIComponent(credentials.password),
                method: "POST",
                dataType: "json",
                contentType: "application/x-www-form-urlencoded",
                success: resolve,
                error: reject
            });
        });
    },
}
