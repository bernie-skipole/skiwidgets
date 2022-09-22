import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'ConfirmBox1'
    # A textblock contains the widget description
    ref = "widgets.confirm.ConfirmBox1"
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



def show_widget(skicall):
    "Called by a button to show the confirmbox"
    if ('buttonlink2', 'get_field1') not in skicall.call_data:
       raise FailPage(message="Invalid call")

    if skicall.call_data['buttonlink2', 'get_field1'] != 'show':
      raise FailPage(message="Invalid call")

    pd = PageData()
    pd['confirmbox1', 'hide'] = False
    skicall.update(pd)


def cancel(skicall):
    "Responds to cancel submission from confirmbox1"

    pd = PageData()
    pd['confirmbox1', 'hide'] = True
    pd['result', 'para_text'] = "The operation has been cancelled"
    skicall.update(pd)


def confirm(skicall):
    "Responds to confirm submission from confirmbox1"

    pd = PageData()
    pd['confirmbox1', 'hide'] = True
    pd['result', 'para_text'] = "The operation has been confirmed"
    skicall.update(pd)

