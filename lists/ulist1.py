import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'UList1'
    # A textblock contains the widget description
    ref = "widgets.lists.UList1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: lists"
    headersection['tomodule','link_ident'] = skicall.makepath('lists')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # fill in the SubmitTextInput4 widget and the UList1 widget with initial values
    pd = PageData()
    pd['setlistdata','input_text'] = "one,two,three"
    pd['ulist1','contents'] = ['one', 'two', 'three']
    skicall.update(pd)



def respond(skicall):
    """Responds to submission from the SubmitTextInput4 widget form.
       Called by an AllowStore responder with general_json page as its
       target so the UList1 widget is updated via a JSON responce,
       and dynamically updates the page."""

    if ('setlistdata', 'input_text') not in skicall.call_data:
        raise FailPage(message="No submission received")

    pd = PageData()
    pd['ulist1','contents'] = skicall.call_data['setlistdata', 'input_text'].split(',')
    skicall.update(pd)

