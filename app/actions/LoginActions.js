var dispatcher = require("../dispatcher");

module.exports = {
    submitLoginCredentials:function(payload){
        dispatcher.dispatch({
           loginPayload:payload,
           type:"login:submitLoginCredentials" 
        });
    },
}
