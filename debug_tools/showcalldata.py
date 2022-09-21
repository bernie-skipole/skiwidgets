import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'ShowCallData'
    # A textblock contains the widget description
    ref = "widgets.debug_tools.ShowCallData"
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
    "Responds to submission from the SubmitTextInput4 widget form"

    if ('setcalldata', 'input_text') not in skicall.call_data:
        raise FailPage(message="No submission received")

    value = skicall.call_data['setcalldata', 'input_text']
    pd = PageData()
    pd['result','para_text'] = f"Received: {value}"
    skicall.update(pd)
