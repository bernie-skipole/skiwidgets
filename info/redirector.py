import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'Redirector'
    # A textblock contains the widget description
    ref = "widgets.info.Redirector"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: info"
    headersection['tomodule','link_ident'] = skicall.makepath('info')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)


def submit_redirection(skicall):
    "Called to submit a redirection URL"

    if ('submittext', 'input_text') not in skicall.call_data:
        raise FailPage(message="No submission received")

    newurl = skicall.call_data['submittext', 'input_text']
    # sanitise newurl
    if not newurl:
        raise FailPage("URL not accepted")
    if not newurl.isascii():
        raise FailPage("URL not accepted: This example only accepts simple URL's")
    for c in " <>%&+=\"\'?(),{}":
        if c in newurl:
            raise FailPage("URL not accepted: This example only accepts simple URL's")

    pd = PageData()
    pd["redirector","url"] = newurl
    skicall.update(pd)
