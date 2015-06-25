Pygments lexer for Robot Framework test data
============================================

This project implements a `Pygments <http://pygments.org>`_ lexer
for `Robot Framework <http://robotframework.org>`_ test data in plain
text format. It is available as a separate plugin and *included in
Pygments 1.6 and newer*.

What is Pygments
----------------

Pygments_ is a generic library/tool for syntax highlighting. It is used by
many different applications and wikis.

What is Robot Framework
-----------------------

`Robot Framework`_ is a generic test automation framework suitable both for
normal test automation and Acceptance Test Driven Development (ATDD). Its
test data is defined in tabular format either in plain text, TSV, or HTML
files. This project provides syntax highlighting for the plain text format.

Installation
------------

.. code-block:: bash

    pip install pygments
    pip install robotframeworklexer

The latter step is only needed if you want to use a newer lexer version than
the one included in Pygments.

Usage
-----

After installation Pygments will recognize ``robotframework``
lexer. It can be used, for example, with the ``pygmentize`` tool:

.. code-block:: bash

    # Lexer for ``*.robot`` files is found automatically.
    pygmentize tests.robot

    # Explicit lexer configuration needed with ``*.txt`` files.
    pygmentize -l robotframework tests.txt

    # Override built-in robotframework lexer with separately installed version.
    pygmentize -O robotframework=robotframework tests

See `generate.py <https://bitbucket.org/robotframework/pygmentslexer/src/default/generate.py>`_
script for an example of the programmatic usage. For general information about
using Pygments, consult `its documentation <http://pygments.org/docs/>`_ and/or
the documentation of the tool you are using it with.

Example
-------

The example below ought to be highlighted using Pygments and this lexer:

.. code-block:: robotframework

    *** Settings ***
    Documentation    Simple example demonstrating syntax highlighting.
    Library          ExampleLibrary
    Test Setup       Keyword    argument   argument with ${VARIABLE}

    *** Variables ***
    ${VARIABLE}      Variable value
    @{LIST}          List    variable    here

    *** Test Cases ***
    Keyword-driven example
        Initialize System
        Do Something
        Result Should Be    42
        [Teardown]    Cleanup System

    Data-driven example
        [Template]    Keyword
        argument1   argument2
        argument    ${VARIABLE}
        @{LIST}

    Gherkin
        Given system is initialized
        When something is done
        Then result should be "42"

    | Pipes |
    |  | [Documentation] | Also pipe separated format is supported. |
    |  | Log | As this example demonstrates. |

    *** Keywords ***
    Result Should Be
        [Arguments]    ${expected}
        ${actual} =    Get Value
        Should be Equal    ${actual}    ${expected}

    Then result should be "${expected}"
        Result Should Be    ${expected}

License
-------

`Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_.
