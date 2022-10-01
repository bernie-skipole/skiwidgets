import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'InputTable1'
    # A textblock contains the widget description
    ref = "widgets.inputtables.InputTable1"
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

    # populate the table
    pd = PageData()
    pd['inputtable1','col1'] = ["1 one", "1 two", "1 three", "1 four"]
    pd['inputtable1','col2'] = ["2 one", "2 two", "2 three", "2 four"]

    pd['inputtable1', 'inputdict'] = {'aaa':'input1', 'bbb':'input2', 'ccc':'input3', 'ddd':'input4'}
    skicall.update(pd)

 
def respond(skicall):
    """Responds to submission from textinput2 which is contained in form1
       The AllowStore responder calling this function has as its target the
       SubmitData responder which calls the above index function. So the
       returned HTML page has both the sections completed and those widgets
       set here completed"""

    if ('textinput2', 'input_text') not in skicall.call_data:
        raise FailPage(message="No submission received")

    pd = PageData()
    pd['result','para_text'] = "Text Received : " + skicall.call_data['textinput2', 'input_text']
    # And fill in the textinput2 field so the last submission remains visible
    if skicall.call_data['textinput2', 'input_text']:
        pd['textinput2', 'input_text'] = skicall.call_data['textinput2', 'input_text']
        # and set the field to geen, to show input has been accepted
        pd['textinput2', 'set_input_accepted'] = True
    else:
        # empty text, set the field to red
        pd['textinput2', 'set_input_errored'] = True
    skicall.update(pd)

