import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'HeadText'
    # A textblock contains the widget description
    ref = "widgets.headers.HeadText"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: headers"
    headersection['tomodule','link_ident'] = skicall.makepath('headers')
    skicall.update(headersection)

    # A SubmitDropDown1 widget with name setheadertag needs its option_list setting
    pd = PageData()
    pd['setheadertag','option_list'] = ["h6", "h5", "h4", "h3", "h2", "h1", "p"]
    skicall.update(pd)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)



def settext(skicall):
    """Responds to submission from the SubmitTextInput4 widget form.
       Called by an AllowStore responder with general_json page as its
       target so the headtext widget is updated via a JSON responce,
       and dynamically updates the page."""

    if ("setheadertext","input_text") not in skicall.call_data:
        raise FailPage(message="No submission received")

    pd = PageData()
    pd['headtext','large_text'] = skicall.call_data["setheadertext","input_text"]

    skicall.update(pd)


def settag(skicall):
    """Responds to submission from the SubmitDropDown1 widget form.
       Called by an AllowStore responder with general_json page as its
       target so the headtext widget is updated via a JSON responce,
       and dynamically updates the page."""

    if ("setheadertag","selectvalue") not in skicall.call_data:
        raise FailPage(message="No submission received")

    if skicall.call_data["setheadertag","selectvalue"] not in ["h6", "h5", "h4", "h3", "h2", "h1", "p"]:
        raise FailPage(message="Invalid submission received")

    pd = PageData()
    pd['headtext','tag'] = skicall.call_data["setheadertag","selectvalue"]

    skicall.update(pd)

    
