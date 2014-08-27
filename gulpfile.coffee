gulp    = require 'gulp'
coffee  = require 'gulp-coffee'
sass    = require 'gulp-sass'

coffeeSrcPath = 'application/assets/coffee/**/*.coffee'
sassSrcPath = 'application/assets/sass/**/*.scss'

gulp.task 'compile-coffee', () ->
    gulp.src coffeeSrcPath
        .pipe coffee()
        .pipe gulp.dest('public/js/')

gulp.task 'compile-sass', () ->
    gulp.src sassSrcPath
        .pipe sass()
        .pipe gulp.dest('public/css/')

gulp.task 'watch', () ->
    gulp.watch(coffeeSrcPath, ['compile-coffee'])
    gulp.watch(sassSrcPath, ['compile-sass'])

gulp.task 'default', ['compile-coffee']
