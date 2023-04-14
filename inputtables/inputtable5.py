import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

# Normally table data would be taken from a file or database or other source of data.
TABLECOL = ["one", "two", "three", "four"]


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'InputTable5'
    # A textblock contains the widget description
    ref = "widgets.inputtables.InputTable5"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: inputtables"
    headersection['tomodule','link_ident'] = skicall.makepath('inputtables')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    pd = PageData()
    pd['inputtable5','col_label'] = TABLECOL
    pd['inputtable5','col_input'] = TABLECOL
    # The hidden field is used to check which row has been submitted
    pd['inputtable5','hidden_field1'] = TABLECOL
    skicall.update(pd)


def respond(skicall):
    "Responds to a table button being pressed"

    if ('inputtable5','hidden_field1') not in skicall.call_data:
        raise FailPage(message="Invalid submission received")

    try:
        # the hidden field should return a string from TABLECOL which
        # has index position equal to the row of the table
        row = TABLECOL.index(skicall.call_data['inputtable5','hidden_field1'])
    except:
        raise FailPage(message="Invalid submission received")

    pd = PageData()
    result = skicall.call_data['inputtable5','col_input']
    submit1 = skicall.call_data.get(('inputtable5','button_text1'))
    submit2 = skicall.call_data.get(('inputtable5','button_text2'))
    if submit1:
        pd['result', 'para_text'] = f"Received: Row {row} {submit1} pressed - data: {result}"
    elif submit2:
        pd['result', 'para_text'] = f"Received: Row {row} {submit2} pressed - data: {result}"
    else:
        raise FailPage(message="Invalid submission received")

    if 2 < len(result) < 6 :
        pd['inputtable5','set_input_accepted'] = {row:True}
        pd['inputtable5','set_input_errored'] = {row:False}
    else:
        pd['inputtable5','set_input_accepted'] = {row:False}
        pd['inputtable5','set_input_errored'] = {row:True}

    skicall.update(pd)
