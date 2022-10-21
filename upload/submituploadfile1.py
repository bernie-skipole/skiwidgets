import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'SubmitUploadFile1'
    # A textblock contains the widget description
    ref = "widgets.upload.SubmitUploadFile1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: upload"
    headersection['tomodule','link_ident'] = skicall.makepath('upload')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)



def respond(skicall):
    """Responds to submission from the SubmitUploadFile1 widget.
       Called by an AllowStore responder with the index page as its
       target. Updates a paras.ParaText widget which shows the result."""

    if ('submituploadfile1','action') not in skicall.call_data:
        raise FailPage(message="No SubmitUploadFile1 received")
    data_received = skicall.call_data['submituploadfile1','action']

    pd = PageData()
    if data_received:
        if len(data_received)>20:
            pd['result','para_text'] = f"Received data: {data_received[:20]} ...."
        else:
            pd['result','para_text'] = f"Received data: {data_received}"
    else:
        pd['result','para_text'] = "No file received"
    skicall.update(pd)

