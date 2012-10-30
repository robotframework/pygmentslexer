#!/bin/sh

root=`dirname $0`
out=$root/tmp/out.html
styles=$root/tmp/styles.css
tests=$root/tests.txt

pygmentize -S autumn -f html > $styles
echo '<html><head>' > $out
echo '<link rel="stylesheet" type="text/css" href="styles.css">' >> $out
echo '</head><body>' >> $out
pygmentize -f html -l robotframework -o $out-2 $tests
cat $out-2 >> $out
echo '</body></html>' >> $out
echo $out
