import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'Circle'
    # A textblock contains the widget description
    ref = "widgets.svgbasics.Circle"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: svgbasics"
    headersection['tomodule','link_ident'] = skicall.makepath('svgbasics')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)


def respond(skicall):
    "Responds to submission from buttonlink2 to change the color of the Circle widget"

    if ('buttonlink2', 'get_field1') not in skicall.call_data:
        raise FailPage(message="No submission received")

    value = skicall.call_data['buttonlink2', 'get_field1']
    if value == 'yellow':
        new_value = 'red'
    elif value == 'red':
        new_value = 'yellow'
    else:
        return
    pd = PageData()
    pd['buttonlink2', 'get_field1'] = new_value
    pd['circle', 'fill'] = new_value
    skicall.update(pd)

    
