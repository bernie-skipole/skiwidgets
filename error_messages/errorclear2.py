import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'ErrorClear2'
    # A textblock contains the widget description
    ref = "widgets.error_messages.ErrorClear2"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: error_messages"
    headersection['tomodule','link_ident'] = skicall.makepath('error_messages')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)



def show_error(skicall):
    "Called by a button to show the ErrorClear2 widget"
    if ('buttonlink2', 'get_field1') not in skicall.call_data:
       raise FailPage(message="Invalid call")

    if skicall.call_data['buttonlink2', 'get_field1'] != 'show error':
      raise FailPage(message="Invalid call")

    # raise an error to be shown in the ErrorClear2 widget
    raise FailPage(message = 'This is an error message', widget='errorclear2')


