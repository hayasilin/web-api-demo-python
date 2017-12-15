*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Test Cases ***
testget
    ${payload}=    Create Dictionary    eid=1
    Create Session    event    http://127.0.0.1:8000/api
    ${r}=    Get Request    event    /get_event_list/    params=${payload}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}
    #断言结果
    ${msg}    Get From Dictionary    ${dict}   message
    Should Be Equal    ${msg}    success
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}

testpost
    Create Session    event    http://127.0.0.1:8000/api
    &{headers}    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    &{payload}=    Create Dictionary    eid=1
    ${r}=    Post Request    event    /add_event/    data=${payload}    headers=${headers}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}
    #断言结果
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    parameter error
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(10021)
    Should Be Equal    ${sta}    ${status}

test_user_sign_success
    Create Session    sign    http://127.0.0.1:8000/api
    &{headers}    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    #Set the parameter
    &{payload}=    Create Dictionary    eid=1    phone=004
    ${r}=    Post Request    sign    /user_sign/    data=${payload}    headers=${headers}
    Should Be Equal As Strings    ${r.status_code}    200
    log    ${r.json()}
    ${dict}    Set variable    ${r.json()}
    #Assertation
    ${msg}    Get From Dictionary    ${dict}    message
    Should Be Equal    ${msg}    sign success
    ${sta}    Get From Dictionary    ${dict}    status
    ${status}    Evaluate    int(200)
    Should Be Equal    ${sta}    ${status}
