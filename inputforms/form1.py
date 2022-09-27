import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'Form1'
    # A textblock contains the widget description
    ref = "widgets.inputforms.Form1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

 
def respond(skicall):
    """Responds to submission from textinput2 which is contained in form1"""

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

