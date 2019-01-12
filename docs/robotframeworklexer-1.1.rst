=========================
Robot Framework Lexer 1.1
=========================

.. default-role:: code

Robot Framework Lexer is a plugin for Pygments_ providing support for syntax highlighting.

Robot Framework Lexer 1.1 is a new release providing Python 3 compatible and support for
new syntax introduced in `Robot Framework 3.1
<https://github.com/robotframework/robotframework/blob/master/doc/releasenotes/rf-3.1.rst>`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframeworklexer

to install the latest release or use

::

   pip install robotframeworklexer==1.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Robot Framework Lexer 1.1 was released on Sunday January 13, 2019.

.. _Pygments: http://pygments.org/
.. _Issue tracker: https://github.com/robotframework/robotframeworklexer/issues?q=milestone%3Av1.1
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframeworklexer


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1`_
      - bug
      - critical
      - Python 3 compatibility
    * - `#5`_
      - enhancement
      - critical
      - Support `Tasks` header and task related aliases for settings like `Task Setup`
    * - `#8`_
      - enhancement
      - critical
      - Support for loops with `FOR` marker and ending them with `END`
    * - `#3`_
      - enhancement
      - high
      - Support nested variable item access like `${var}[0][key]`
    * - `#10`_
      - enhancement
      - medium
      - Unknown headers should be marked as errors
    * - `#2`_
      - enhancement
      - medium
      - Don't support `*.txt` files
    * - `#4`_
      - enhancement
      - medium
      - Remove support for headers and settings not anymore support by Robot Framework
    * - `#7`_
      - enhancement
      - medium
      -  Remove support for using for loop separators like `IN` case- and space-insensitively
    * - `#9`_
      - bug
      - low
      - `IN ENUMERATE` and `IN ZIP` for loops not correctly supported
    * - `#6`_
      - enhancement
      - low
      - Remove support for using headers and settings space-insensitively

Altogether 10 issues. View on the `issue tracker <https://github.com/robotframework/pygmentslexer/issues?q=milestone%3Av1.1>`__.

.. _#1: https://github.com/robotframework/pygmentslexer/issues/1
.. _#5: https://github.com/robotframework/pygmentslexer/issues/5
.. _#8: https://github.com/robotframework/pygmentslexer/issues/8
.. _#3: https://github.com/robotframework/pygmentslexer/issues/3
.. _#10: https://github.com/robotframework/pygmentslexer/issues/10
.. _#2: https://github.com/robotframework/pygmentslexer/issues/2
.. _#4: https://github.com/robotframework/pygmentslexer/issues/4
.. _#7: https://github.com/robotframework/pygmentslexer/issues/7
.. _#9: https://github.com/robotframework/pygmentslexer/issues/9
.. _#6: https://github.com/robotframework/pygmentslexer/issues/6
