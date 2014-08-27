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

gulp.task 'js-compile', () ->
    compileFileName = 'application.js'
    gulp.src [ paths.jsSrc, '!' + paths.jsDest + '/' + compileFileName ]
        .pipe concat(compileFileName)
        .pipe uglify()
        .pipe gulp.dest(paths.jsDest)

gulp.task 'compile-sass', () ->
    gulp.src paths.sassSrc
        .pipe sass()
        .pipe gulp.dest(paths.cssDest)

gulp.task 'css-compile', () ->
    compileFileName = 'application.css'
    gulp.src [ paths.cssSrc, '!' + paths.cssDest + "/" + compileFileName ]
        .pipe concat(compileFileName)
        .pipe minifyCss()
        .pipe gulp.dest(paths.cssDest)

gulp.task 'watch', () ->
    gulp.watch paths.coffeeSrc, ['compile-coffee', 'js-compile']
    gulp.watch paths.sassSrc, ['compile-sass', 'css-compile']

gulp.task 'assets-compile', ['compile-coffee', 'compile-sass', 'js-compile', 'css-compile']

gulp.task 'default', ['watch']
