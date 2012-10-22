#!/bin/sh

pygmentize -S default -f html > styles.css
echo '<html><head>' > out.html
echo '<link rel="stylesheet" type="text/css" href="styles.css" media="all">' >> out.html
echo '</head><body>' >> out.html
pygmentize -f html -l robotframework tests.txt >> out.html
echo '</body></html>' >> out.html
