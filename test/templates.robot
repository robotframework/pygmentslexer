*** Settings ***
Test template    keyword


*** Test cases ***
Template from settings
    arg1    arg2
    ${var}  arg2
    arg1    ${var}
    @{list}

Overriden template
   [template]    custom keyword
    arg1    arg2
    ${var}  arg2
    arg1    ${var}
    @{list}

No template
   [template]
   Keyword    arg1
   ${assign}    Keyword2    arg

No template 2
   [ T E M P L A T E ]    NoNe
   Keyword    arg1
   ${assign}    Keyword2    arg

Template again
    arg1    arg2
    ${var}  arg2
    arg1    ${var}
    @{list}

