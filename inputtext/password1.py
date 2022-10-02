import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'Password1'
    # A textblock contains the widget description
    ref = "widgets.inputtext.Password1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: inputtext"
    headersection['tomodule','link_ident'] = skicall.makepath('inputtext')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

 
def respond(skicall):
    """Responds to submission from password1 which is contained in form1
       The AllowStore responder calling this function has as its target the
       SubmitData responder which calls the above index function. So the
       returned HTML page has both the sections completed and those widgets
       set here completed"""

    if ('password1', 'input_text') not in skicall.call_data:
        raise FailPage(message="No submission received")

    pd = PageData()
    # And check the password1 field
    if skicall.call_data['password1', 'input_text'] == "password":
        # and set the field to geen, to show input has been accepted
        pd['password1', 'set_input_accepted'] = True
        pd['result','para_text'] = "Correct password received!"
    else:
        # bad password, set the field to red
        pd['password1', 'set_input_errored'] = True
        pd['result','para_text'] = "Incorrect text received : " + skicall.call_data['password1', 'input_text']
    skicall.update(pd)

