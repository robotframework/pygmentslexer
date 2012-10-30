#!/bin/sh

root=`dirname $0`
out=$root/tmp/out.html
styles=$root/tmp/styles.css
tests=$root/tests.txt

pygmentize -S autumn -f html > $styles
echo '<html><head>' > $out
echo '<link rel="stylesheet" type="text/css" href="styles.css">' >> $out
echo '</head><body>' >> $out
pygmentize -f html -l robotframework $tests >> $out
echo '</body></html>' >> $out
echo $out
