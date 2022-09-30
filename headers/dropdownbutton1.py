import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'DropDownButton1'
    # A textblock contains the widget description
    ref = "widgets.headers.DropDownButton1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: headers"
    headersection['tomodule','link_ident'] = skicall.makepath('headers')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # The DropDownButton1 widget takes a list of lists, each inner list describing a link
    # For each navigation link, the inner list elements are:
    # 0 : The url, label or ident of the target page of the link
    # 1 : The displayed text of the link
    # 2 : If True, ident is appended to link even if there is no get field
    # 3 : The get field data to send with the link

    # set the options in the DropDown1 widget
    pd = PageData()
    pd['dropdownbutton1', 'nav_links'] = [ ["home", "Modules List", False, ''],
                                           ["/skiwidgets/headers/", "Headers Module", False, ''],
                                           ["/skiwidgets/footers/", "Footers Module", False, '']
                                         ]


    skicall.update(pd)

    
