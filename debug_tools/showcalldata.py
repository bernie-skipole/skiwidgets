import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'ShowCallData'
    ref = "widgets.debug_tools.ShowCallData"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    skicall.update(headersection)

    # this code file contents is placed in a pre tag, set in section 'codefile'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # The input text widget is updated with any string input
    if ('setcalldata', 'input_text') in skicall.call_data:
        pd = PageData()
        pd['setcalldata', 'input_text'] = skicall.call_data['setcalldata', 'input_text']
        skicall.update(pd)



