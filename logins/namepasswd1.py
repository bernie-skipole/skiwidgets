import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'NamePasswd1'
    # A textblock contains the widget description
    ref = "widgets.logins.NamePasswd1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: logins"
    headersection['tomodule','link_ident'] = skicall.makepath('logins')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

 
def respond(skicall):
    """Responds to submission from namepasswd1
       The AllowStore responder calling this function has as its target the
       SubmitData responder which calls the above index function. So the
       returned HTML page has both the sections completed and those widgets
       set here completed"""

    if ('namepasswd1', 'input_text1') not in skicall.call_data:
        raise FailPage(message="No username received")

    if ('namepasswd1', 'input_text2') not in skicall.call_data:
        raise FailPage(message="No password received")

    loggedin = False
    if skicall.call_data['namepasswd1', 'input_text1'] == "username" and skicall.call_data['namepasswd1', 'input_text2'] == "password":
        loggedin = True

    pd = PageData()
    if loggedin:
        pd['result','para_text'] = "Correct username and password received!"
    else:
        pd['result','para_text'] = "Invalid username and password received!"
    skicall.update(pd)

