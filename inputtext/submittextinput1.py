import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'SubmitTextInput1'
    # A textblock contains the widget description
    ref = "widgets.inputtext.SubmitTextInput1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: inputtext"
    headersection['tomodule','link_ident'] = skicall.makepath('inputtext')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # populate the widget hidden fields
    pd = PageData()
    pd['submittextinput1', 'hidden_field1'] = "AAA"
    pd['submittextinput1', 'hidden_field2'] = "BBB"
    pd['submittextinput1', 'hidden_field3'] = "CCC"
    pd['submittextinput1', 'hidden_field4'] = "DDD"
    skicall.update(pd)


def respond(skicall):
    """Responds to submission from submittextinput1.
       The AllowStore responder calling this function has general_json
       as its target which updates the page fields"""

    if ('submittextinput1', 'input_text') not in skicall.call_data:
        raise FailPage(message="No submission received")

    # populate the result widget
    pd = PageData()
    pd['result', 'para_text'] = f"Text received: {skicall.call_data['submittextinput1', 'input_text']}"
    skicall.update(pd)
