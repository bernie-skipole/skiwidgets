import os, json

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

# Normally table data would be taken from a file or database or other source of data.
TABLECOL1 = [10, 100, 1000, 10000]
TABLECOL2 = [2, 20, 200, 2000]
TABLEINPUT = {'aaa':5, 'bbb':50, 'ccc':500, 'ddd':5000}


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'InputTable3'
    # A textblock contains the widget description
    ref = "widgets.inputtables.InputTable3"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: inputtables"
    headersection['tomodule','link_ident'] = skicall.makepath('inputtables')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

    if 'tabledone' in skicall.call_data:
        # table is populated, no need to set contents here
        return

    # illustrate the table by filling in initial global values
    pd = PageData()
    pd['inputtable3','col1'] = TABLECOL1
    pd['inputtable3','col2'] = TABLECOL2
    pd['inputtable3', 'inputdict'] = TABLEINPUT.copy()

    skicall.update(pd)


 
def respond(skicall):
    """Called by a GetDictionaryDefaults responder having received a submission
       from inputtable3.
       This responder expects this function to return a dictionary which will be
       updated with the dictionary received from the inputtable3. The responder has
       as its target an AllowStore responder which sets this updated received data
       into skicall.call_data"""

    # This function is necessary since any empty contents may be missing from
    # the submission, and this ensures they are all present

    return {'aaa':'', 'bbb':'', 'ccc':'', 'ddd':''}


def renew(skicall):
    """Renews the table on inputdict being received"""
    if ('inputtable3', 'inputdict') not in skicall.call_data:
        raise FailPage(message="No submission received")
    try:
        inputdict = skicall.call_data['inputtable3', 'inputdict']
        rowlist = ['aaa', 'bbb', 'ccc', 'ddd']
        pd = PageData()
        pd['inputtable3', 'inputdict'] = {key:inputdict[key] for key in rowlist}
        skicall.update(pd)
    except:
        raise FailPage(message="Invalid submission received")
    # now call index(skicall) to fill in the page again, but flag data is present
    skicall.call_data['tabledone'] = True
    index(skicall)
    

