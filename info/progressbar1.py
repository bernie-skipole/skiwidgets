import os, time

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'ProgressBar1'
    # A textblock contains the widget description
    ref = "widgets.info.ProgressBar1"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: info"
    headersection['tomodule','link_ident'] = skicall.makepath('info')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    # Add a timestamp to the page at which the progress bar starts
    pd = PageData()
    pd.ident_data = str(time.time())
    skicall.update(pd)


def refreshbar(skicall):
    "Refresh the bar  - complete after 30 seconds"
    pd = PageData()
    try:
        barzero = float(skicall.ident_data)
    except:
        # invalid value in ident_data, so start bar from zero
        pd["progressbar1", "value"] = 0
        pd.ident_data = str(time.time())
        skicall.update(pd)
        return
    timenow = time.time()
    if timenow < barzero:
        # something wrong, server time change? so start again
        pd["progressbar1", "value"] = 0
        pd.ident_data = str(time.time())
        skicall.update(pd)
        return
    if timenow >= barzero+30:
        # bar is complete
        pd["progressbar1", "value"] = 100
        pd.interval = 0
        skicall.update(pd)
        return
    # so timenow is between barzero and barzero + 30
    pd["progressbar1", "value"] = (100 * (timenow - barzero))//30
    skicall.update(pd)

 
