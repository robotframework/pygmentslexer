Stuff before first table is considered comment.
...    and there is no continuing here.

*** Settings ***
...              Error
Documentation    Hyvää päivää    ${var}
Library          XML    arg
Resource         ${foobar}.txt    # comment
Test setup       keyword    argument    ${variable}
Test Teardown    ${keyword}    argument    ${argument}
Metadata         Name    Value
metadata         Valid      because settings are case-insensitive
Meta data        Invalid    because settings are space-sensitive
Suitesetup       Settings are space-sensitive
Nonex            Non-existing setting

| Force tags  |  regression  | ${var}
| ...         |  more        | tags |
# comment

*variable
...               error
${VARIABLE}       value
${ASSIGNMENT}=    value
@{LIST}           value 1    ${var}    \${not}    \\${var}    \\\${not}    # comment
...               value # not comment
&{DICT}           Key1=Value1    Key2=Value2    Key${3}=${value3}
INVALID           syntax
${IN} ${VALID}    syntax
${INV} ==         syntax

#| @{VARIABLE} | value 1 | value 2 | value 3
| @{VARIABLE} | value 1 | value 2 | value 3 | # comment | here |
|    @{VARIABLE}    |     value  1     | %{ENV} | value 3
| @{VARIABLE} | ${var${inside}} out} | @{${var${not}} | value 3|
| @{VARIABLE} | @{VARIABLE}[0] | @{VARIABLE}[${i}] | value 3 |


| *** Test Case *** | *** Action *** | *** Argument *** |
Example
    Keyword    arg    arg ${with var}    # comment
    Keyword    arg    arg ${with var}    # comment
    [teardown]    keyword    arg

Example 2    [Documentation]    example
    [ tags ]    foo    # comment
    Keyword    arg    arg ${with var}    # comment
    ${var} =    keyword
    ${var}    keyword    ${arg}   ${two} vars ${here}    arg   arg    arg
    Trailing spaces
    ${v1}    ${v2}    @{v3} =    keyword

Variable items
    Log Many    ${var}[0]    ${var}[key]    ${var}[${item}]    ${var}[0][key][ ${item} ]
    Log Many    @{var}[0]    &{var}[key]
    Log Many    ${var}\[0]    @{var}\[0]    &{var}\[0]
...
    Keyword    arg1
    ...    ${arg2}
    ${var} =    Keyword    arg1
    ...    ${arg2}
    ${var} =
    ...    Keyword    arg1
    ...    ${arg2}
    ${var1}    ${var2} =    Keyword    arg1
    ...    ${arg2}
    ${var1}
    ...    ${var2} =
    ...    Keyword    arg1    ${arg2}
    ...    arg3
    ...
    ...    arg4

Template
    [Template]    Keyword Here
    args       here
    ${more}    args

Template 2
    [ template ]    Keyword Here
    args       here
    ${more}    args

| Pipes |
|  | [Documentation] | Also pipe separated format is supported |
|  | Should Be Equal |  | ${EMPTY} |
|  | Should Be Equal |     | ${EMPTY}
| |     Log Many     | |foo | bar| | \| | |zap|
| |     Log Many     | | |

FOR
    FOR    ${x}    IN    foo    bar
        Log    ${x}
    END
    No Operation
    FOR    ${x}    IN    ${1}    two    3
    ...    neljä    ${6} - 1
        Log    ${x}
    END
    FOR    ${i}
    ...    IN RANGE    42
        ${ret} =    Keyword    ${i}
        ...    more    args
    END
    FOR    ${index}    ${item}    IN ENUMERATE    @{STUFF}
        No Operation
    END
    FOR    ${a}    ${b}    ${c}    IN ZIP    ${X}    ${Y}    ${Z}
        No Operation
    END
    Log    ...

Old :FOR
    :FOR    ${x}    IN    foo    bar
    \    Log    ${x}
    No Operation
    :FOR    ${x}    IN    ${1}    two    3
    ...    neljä    ${6} - 1
    \    Log    ${x}
    :: FOR    ${i}
    ...    IN RANGE    42
    \    ${ret} =    Keyword    ${i}
    \    ...    more    args
    : F O R    ${index}    ${item}    IN ENUMERATE    @{STUFF}
    \    No Operation
    :FOR    ${a}    ${b}    ${c}    IN ZIP    ${X}    ${Y}    ${Z}
    \    No Operation
    Log    ...

Invalid FOR
    FOR    ${x}    in    should    be    upper
        No Operation
    END
    No Operation
    FOR    x    IN    item    should    be    variable
        No Operation
    END
    No Operation
    F O R    ${x}    IN    for    is    space-sensitive
        No Operation
    E N D
    for    ${x}    IN    for    is    case-sensitive
        No Operation
    end


*** Keywords ***    Heading    # Comment     here

XXX
    [Documentation]    hello
    [Tags]  whatever
    kw    arg
    ${var} =    kw    ${var}
    [Teardown]    keyword    arg1    ${var}
    [Return]    ${var}

Given ${variable} handling works out-of-the-box
    No Operation

Invalid settings
    [nonex]        Non-existing settings
    [Tear Down]    Settings are space-sensitive
    [ Setup ]      Spaces around are allowed
    [timeout]      Settings are case-insensitive

*** Nonex ***
Header above should be invalid because it has non-existing header.

*** Nonex ***    FOO    BAR
The whole header row above should be invalid because it has non-existing header.

*** TestCase ***
Header above should be invalid because headers are space-sensitive.

***Settings***
Default Tags    Spaces around are optional, though.

*** variable ***
${VAR}          Headers are case-insensitive.

*** Comment ***
Comment headers are allowed and can contain whatever data.

Data is considered to be comment. No highlighting for
${variables} or
...    continuation or anything like that.

THE END
