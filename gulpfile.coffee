gulp        = require 'gulp'
coffee      = require 'gulp-coffee'
uglify      = require 'gulp-uglify'
sass        = require 'gulp-sass'
minifyCss   = require 'gulp-minify-css'
concat      = require 'gulp-concat'
clean       = require 'gulp-clean'

paths =
    coffeeSrc: 'application/assets/coffee/**/*.coffee'
    sassSrc: 'application/assets/sass/**/*.scss'
    jsSrc: 'public/js/**/*.js'
    cssSrc: 'public/css/**/*.css'
    cssDest: 'public/css/'
    jsDest: 'public/js'

gulp.task 'compile-coffee', () ->
    gulp.src paths.coffeeSrc
        .pipe coffee()
        .pipe gulp.dest(paths.jsDest)

gulp.task 'js-precompile', () ->
    gulp.src paths.jsSrc
        .pipe clean('application.js')
        .pipe concat('application.js')
        .pipe uglify()
        .pipe gulp.dest(paths.jsDest)

gulp.task 'css-precompile', () ->
    gulp.src paths.cssSrc
        .pipe clean('application.css')
        .pipe concat('application.css')
        .pipe minifyCss()
        .pipe gulp.dest(paths.cssDest)

gulp.task 'compile-sass', () ->
    gulp.src paths.sassSrc
        .pipe sass()
        .pipe gulp.dest(paths.cssDest)

gulp.task 'watch', () ->
    gulp.watch(paths.coffeeSrc, ['compile-coffee'])
    gulp.watch(paths.sassSrc, ['compile-sass'])

gulp.task 'default', ['compile-coffee', 'compile-sass', 'js-precompile', 'css-precompile']
