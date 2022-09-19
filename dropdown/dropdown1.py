import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    # the title and widget decription is in section 'header'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'DropDown1'
    # A textblock contains the widget description
    ref = "widgets.dropdown.DropDown1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    skicall.update(headersection)

    # this code file contents is placed in a pre tag, set in section 'codefile'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # set the options in the DropDown1 widget
    pd = PageData()
    pd['dropdown1', 'option_list'] = ["One", "Two", "Three", "Four"]
    pd['dropdown1', 'selectvalue'] = "Two"
    skicall.update(pd)


def respond(skicall):
    "Responds to submission from DropDown1"

    if ('dropdown1', 'selectvalue') not in skicall.call_data:
        raise FailPage(message="No DropDown1 submission received")

    value = skicall.call_data['dropdown1', 'selectvalue']
    if value not in ["One", "Two", "Three", "Four"]:
        raise FailPage(message="An invalid value has been received")
    # A valid value has been picked, display it as a result
    pd = PageData()
    pd['result','para_text'] = f"The value {value} has been submitted."
    skicall.update(pd)

 
