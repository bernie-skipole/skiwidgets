import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'BooleanRadio'
    # A textblock contains the widget description
    ref = "widgets.radio.BooleanRadio"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: radio"
    headersection['tomodule','link_ident'] = skicall.makepath('radio')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)
    


def respond(skicall):
    """Responds to submission from the BooleanRadio widget.
       Called by an AllowStore responder with general_json page as its
       target so the result widget is updated via a JSON responce,
       and dynamically updates the page."""

    if ('booleanradio', 'radio_checked') not in skicall.call_data:
        raise FailPage(message="No BooleanRadio submission received")

    pd = PageData()
    if skicall.call_data['booleanradio', 'radio_checked'] == 'True':
        # The True button is checked
        pd['result','para_text'] = "The option chosen is True"
    else:
        # The False button is checked
        pd['result','para_text'] = "The option chosen is False"
    skicall.update(pd)
