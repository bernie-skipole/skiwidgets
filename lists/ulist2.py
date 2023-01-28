import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'UList2'
    # A textblock contains the widget description
    ref = "widgets.lists.UList2"
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

    # fill in the UList2 widget with initial values
    pd = PageData()
    pd['ulist2','set_html'] = ['<h1>one</h1>', '<h2>two</h2>', '<h3>three</h3>', '<h4>four</h4>']
    skicall.update(pd)


def toggle(skicall):
    "Called by button to toggle the highlight class and contents of the UList2 widget"

    if ("set_highlight","get_field1") not in skicall.call_data:
        raise FailPage(message="No submission received")

    pd = PageData()
    value = skicall.call_data["set_highlight","get_field1"]
    if value == "set":
        pd["ulist2", "set_highlight"] = True
        pd["set_highlight", "get_field1"] = "unset"
        pd['ulist2','set_html'] = ['<h4>four</h4>', '<h3>three</h3>', '<h2>two</h2>', '<h1>one</h1>']
    elif value == "unset":
        pd["ulist2", "set_highlight"] = False
        pd["set_highlight", "get_field1"] = "set"
        pd['ulist2','set_html'] = ['<h1>one</h1>', '<h2>two</h2>', '<h3>three</h3>', '<h4>four</h4>']
    else:
        raise FailPage(message="Invalid submission received")
    skicall.update(pd)





