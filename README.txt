<<TableOfContents()>>

= Introduction =

This project implements a [[http://www.pygments.org/|Pygments]] lexer
for [[http://robotframework.org|Robot Framework]] test data in plain
text format. When the lexer is mature enough, we hope that it will be
incorporated with Pygments.

= What is Robot Framework =

[[http://robotframework.org|Robot Framework]] is a generic test
automation framework suitable both for normal test automation and
Acceptance Test Driven Development (ATDD). Its test data is defined in
tabular format either in plain text, TSV, or HTML files.

= What is Pygments =

[[http://www.pygments.org/|Pygments]] is a generic library/tool for
syntax highlighting. It is used by many different applications and
wikis, including the wiki here in BitBucket.

= Installation =

{{{
$ pip install robotframeworklexer
}}}

This will automatically install also Pygments if you do not already
have it. If/when this lexer is bundled with Pygments, you only need to
install Pygments.

= Usage =

After installation Pygments will recognize //robotframework//
lexer. It can be used, for example, with //pygmentize// tool:

{{{
$ pygmentize -l robotframework tests.txt
}}}

See
[[https://bitbucket.org/pekkaklarck/robotframeworklexer/src/default/generate.py|generate.py]]
script for an example of the programmatic usage. For general
information about using Pygments, consult
[[http://pygments.org/docs/|its documentation]] and/or the
documentation of the tool you are using it with.

= Example =

{{{
#!robotframework
}}}

= License =

[[http://www.apache.org/licenses/LICENSE-2.0.html|Apache License, Version 2.0]].
