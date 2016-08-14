var dispatcher = require("../dispatcher");

function TrackStore() {
    var listeners = [];
    _tracks = []

    function onChange(listener) {
        getTracks(listener);
        listeners.push(listener);
    }
    
    function getTracks(cb){
        return _tracks;
    }

    function addTrack(track) {
        // trackService.addTrack(track).then(function (res) {
        //     console.log(res);
        //     triggerListeners();
        // });
    }

    function deleteTrack(track) {
        // trackService.deleteTrack(track).then(function (res) {
        //     console.log(res);
        //     triggerListeners();
        // });
    }

    function triggerListeners() {
        getTracks(function (res) {
            listeners.forEach(function (listener) {
                listener(res);
            });
        });
    }

    dispatcher.register(function (payload) {
        var split = payload.type.split(":");
        if (split[0] === "track") {
            switch (split[1]) {
                case "addTrack":
                    addTrack(payload.track);
                    break;
                case "deleteTrack":
                    deleteTrack(payload.track);
                    break;
            }
        }
    });

    return {
        onChange: onChange
    }
}

module.exports = TrackStore();