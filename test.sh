#!/bin/sh

out=tmp/out.html
styles=tmp/styles.css

pygmentize -S default -f html > $styles
echo '<html><head>' > $out
echo '<link rel="stylesheet" type="text/css" href="styles.css">' >> $out
echo '</head><body>' >> $out
pygmentize -f html -l robotframework tests.txt >> $out
echo '</body></html>' >> $out
