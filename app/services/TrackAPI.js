var $ = require("jquery");
var promise = require("es6-promise");
var resourceUrl = "/audio/upload";

module.exports = {
    uploadAudio: function (files) {
        console.log('uploadAudio...');
        console.dir(files);
        var data = new FormData();
        data.append('audio-file', files[0], 'audio-file');
        var Promise = promise.Promise;
        return new Promise(function (resolve, reject) {
            $.ajax({
                url: resourceUrl,
                data: data,
                method: "POST",
                processData: false,
                contentType: false,
                dataType: "json",
                success: function(){console.log('upload audio success' + '\n')},
                error: function(){console.log('upload audio error' + '\n')}
            });
        });
    }
}