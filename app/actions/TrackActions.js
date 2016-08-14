var dispatcher = require("../dispatcher");

module.exports = {
    addTrack:function(track){
        dispatcher.dispatch({
           track:track,
           type:"track:addTrack" 
        });
    },
    deleteTrack:function(track){
        dispatcher.dispatch({
           track:track,
           type:"track:deleteTrack" 
        });
    }
}
