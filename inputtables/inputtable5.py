import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


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

    # illustrate the table by accepting data from the inputs, and using it to populate col1
    pd = PageData()
    # label column is static
    pd['inputtable5','col_label'] = ["one", "two", "three", "four"]
    pd['inputtable5','col_input'] = ["one", "two", "three", "four"]
    skicall.update(pd)


def respond(skicall):
    "Responds to a table button being pressed"
    pd = PageData()
    if ('inputtable5','col_input') in skicall.call_data:
        result = skicall.call_data['inputtable5','col_input']
        submit1 = skicall.call_data.get(('inputtable5','button_text1'))
        submit2 = skicall.call_data.get(('inputtable5','button_text2'))
        if submit1 == "Submit1":
            pd['result', 'para_text'] = f"Received: Submit1 pressed - data: {result}"
        elif submit2 == "Submit2":
            pd['result', 'para_text'] = f"Received: Submit2 pressed - data: {result}"
        skicall.update(pd)
        



