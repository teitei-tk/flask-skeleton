gulp = require 'gulp'
coffee = require 'gulp-coffee'

gulp.task 'compile-coffee', () ->
    gulp.src 'application/assets/coffee/**/*.coffee'
        .pipe coffee()
        .pipe gulp.dest('public/js/')

gulp.task 'default', ['compile-coffee']
