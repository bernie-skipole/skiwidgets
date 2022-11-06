import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'AlertClear2'
    # A textblock contains the widget description
    ref = "widgets.confirm.AlertClear2"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: confirm"
    headersection['tomodule','link_ident'] = skicall.makepath('confirm')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)



def show_widget(skicall):
    "Called by a button to show the AlertClear2"
    if ('buttonlink2', 'get_field1') not in skicall.call_data:
       raise FailPage(message="Invalid call")

    if skicall.call_data['buttonlink2', 'get_field1'] != 'show':
      raise FailPage(message="Invalid call")

    pd = PageData()
    pd['alertclear2', 'para_text'] = "Text set into the widget by JSON"
    pd['alertclear2', 'hide'] = False
    pd['result', 'para_text'] = "Show widget has been accepted"
    skicall.update(pd)


def show_error(skicall):
    "Called by a button to raise an error on the AlertClear2"
    pd = PageData()
    pd['result', 'para_text'] = "An Error has been raised"
    skicall.update(pd)
    raise FailPage(message="An Error has been raised", widget="alertclear2")


def clear(skicall):
    "Responds to clear submission from alertclear2"
    pd = PageData()
    pd['alertclear2', 'hide'] = True
    pd['result', 'para_text'] = "The message has been accepted"
    skicall.update(pd)





