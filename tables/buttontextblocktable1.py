import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'ButtonTextBlockTable1'
    # A textblock contains the widget description
    ref = "widgets.tables.ButtonTextBlockTable1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: tables"
    headersection['tomodule','link_ident'] = skicall.makepath('tables')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # Fill in the table : A list of lists, an inner list for each row. First item of inner lists
    # is the value on the button, which will be returned when the button is submitted, second item
    # is the TextBlock reference for the second column.

    # this project has a tuple of module names in skicall.proj_data['modules']

    contents = []
    modules_tuple = skicall.proj_data['modules']
    for name in modules_tuple:
        ref = 'widgets.' + name + '.module'
        contents.append([name, ref])

    pd = PageData()
    pd['buttontextblocktable1','buttons'] = contents
    skicall.update(pd)



def respond(skicall):
    """Responds to submission from the ButtonTextBlockTable1 widget.
       Called by an AllowStore responder with the index page as its
       target. Updates a paras.ParaText widget which shows the result."""

    if ('buttontextblocktable1','buttons') not in skicall.call_data:
        raise FailPage(message="No ButtonTextBlockTable1 submission received")
    name_received = skicall.call_data['buttontextblocktable1','buttons']

    pd = PageData()
    if name_received in skicall.proj_data['modules']:
        # A valid module name has been received
        pd['result','para_text'] = f"The module name {name_received} has been received"
    else:
        # Invalid data received
        pd['result','para_text'] = "Received data is invalid"
    skicall.update(pd)

