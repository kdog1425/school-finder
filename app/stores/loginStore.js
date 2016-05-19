var dispatcher = require("../dispatcher");
var loginService = require("../services/LoginService");

function LoginStore() {
    var listeners = [];

    function onChange(listener) {
        listeners.push(listener);
    }

    function handleJWTToken(jwt, loginSuccessCallback){
        localStorage.setItem('jwt', jwt);
        loginSuccessCallback();
    }
    
    function submitLoginCredentials(payload){
        credentials = {email:payload.email, password: payload.password};
        loginService.submitLoginCredentials(credentials).then(function (res) {
            console.log(res);
            if (res.token){
                handleJWTToken(res.token, payload.loginSuccessCallback);
            } else {
                console.log('no token in response');
            }
        });
    }

    dispatcher.register(function (payload) {
        console.log(payload);
        var split = payload.type.split(":");
        if (split[0] === "login") {
            switch (split[1]) {
                case "submitLoginCredentials":
                    submitLoginCredentials(payload.loginPayload);
                    break;
            }
        }
    });

    return {
        onChange: onChange
    }
}

module.exports = LoginStore();
