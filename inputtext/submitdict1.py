import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

DATA = {"one":1, "two":2, "three":3, "four":4}


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'SubmitDict1'
    # A textblock contains the widget description
    ref = "widgets.inputtext.SubmitDict1"
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

    # populate the submitdict1 widget
    pd = PageData()
    data = DATA.copy()
    # if the data has been updated by a call to respond, update the dictionary here
    if ('submitdict1', 'input_dict') in skicall.call_data:
        data.update(skicall.call_data['submitdict1', 'input_dict'])
    pd['submitdict1', 'input_dict'] = data
    skicall.update(pd)


def respond(skicall):
    """Responds to submission from submitdict1.
       The AllowStore responder calling this function has as its target the
       SubmitData responder which calls the above index function. So the
       returned HTML page has both the sections completed and those widgets
       set here completed"""

    if ('submitdict1', 'input_dict') not in skicall.call_data:
        raise FailPage(message="No submission received")
