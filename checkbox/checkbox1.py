import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'CheckBox1'
    # A textblock contains the widget description
    ref = "widgets.checkbox.CheckBox1"
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
    


def respond(skicall):
    "Responds to submission from CheckBox1"

    if ('checkbox1', 'checkbox') not in skicall.call_data:
        raise FailPage(message="No CheckBox1 submission received")

    pd = PageData()
    if skicall.call_data['checkbox1', 'checkbox'] == 'checkbox1set':
        # The checkbox is ticked
        pd['result','para_text'] = "The CheckBox1 is ticked"
    else:
        # The checkbox is not ticked
        pd['result','para_text'] = "The CheckBox1 is not ticked"
    skicall.update(pd)
