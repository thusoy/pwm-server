'use strict';

var gulp = require('gulp'),
    nodeunit = require('gulp-nodeunit');

gulp.task('default', function () {
    gulp.src('pwm_server/static/*test.js')
        .pipe(nodeunit());
});
