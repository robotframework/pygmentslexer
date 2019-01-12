*** Settings ***
Test Template       Keyword

*** Test Cases ***
Template from settings
    arg1    arg2
    ${var}  arg2
    arg1    ${var}
    @{list}

Overriden template
   [Template]    custom keyword
    arg1    arg2
    ${var}  arg2
    arg1    ${var}
    @{list}

No template
   [ template ]
   Keyword    arg1
   ${assign}    Keyword2    arg

No template 2
   [TEMPLATE]    NoNe
   Keyword    arg1
   ${assign}    Keyword2    arg

Template again
    arg1    arg2
    ${var}  arg2
    arg1    ${var}
    @{list}
