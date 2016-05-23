var gulp = require("gulp");
var browserify = require("browserify");
var reactify = require("reactify");
var source = require("vinyl-source-stream");

gulp.task("bundle", function () {
    return browserify({
        entries: "./app/main.jsx",
        debug: true
    }).transform(reactify)
        .bundle()
        .pipe(source("main.js"))
        .pipe(gulp.dest("app/dist"))
});

gulp.task("copy", ["bundle"], function () {
    return gulp.src([
        "app/index.html",
        "app/lib/bootstrap-css/css/bootstrap.min.css",
        "app/style.css",
        "app/lib/mp3/hum-1.mp3",
        "app/lib/mp3/hum-2.mp3",
        "app/lib/mp3/hum-3.mp3",
        ])
        .pipe(gulp.dest("app/dist"));
});

gulp.task("default",["copy"],function(){
   console.log("Gulp completed..."); 
});
