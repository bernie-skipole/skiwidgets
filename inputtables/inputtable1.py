import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'InputTable1'
    # A textblock contains the widget description
    ref = "widgets.inputtables.InputTable1"
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

    # illustrate the table by accepting data from the inputs, and using it to populate col1
    pd = PageData()
    # col2 is static
    pd['inputtable1','col2'] = ["2 one", "2 two", "2 three", "2 four"]

    # col1 is updated with submitted values if they have been received
    if ('inputtable1', 'inputdict') not in skicall.call_data:
        # on the first call to this page ('inputtable1', 'inputdict') will
        # not be in skicall.call_data, so col1 and inputdict are set with initial values
        pd['inputtable1','col1'] = ["1 one", "1 two", "1 three", "1 four"]
        pd['inputtable1', 'inputdict'] = {'aaa':'input1', 'bbb':'input2', 'ccc':'input3', 'ddd':'input4'}
    else:
        # however, after data submission, inputdict will be defined, so update col1
        # and inputdict with the vaues received
        call_data = skicall.call_data['inputtable1', 'inputdict']
        pd['inputtable1','col1'] = [call_data['aaa'], call_data['bbb'], call_data['ccc'], call_data['ddd']]
        pd['inputtable1', 'inputdict'] = {'aaa':call_data['aaa'],
                                          'bbb':call_data['bbb'],
                                          'ccc':call_data['ccc'],
                                          'ddd':call_data['ddd']
                                         }

    skicall.update(pd)

 
def respond(skicall):
    """Called by a GetDictionaryDefaults responder having received a submission
       from inputtable1.
       This responder expects this function to return a dictionary which will be
       updated with the dictionary received from the inputtable1. The responder has
       as its target an AllowStore responder which sets this updated received data
       into skicall.call_data and calls the above index function"""

    # This function is necessary since any empty contents may be missing from
    # the submission, and this ensures they are all present

    return {'aaa':'', 'bbb':'', 'ccc':'', 'ddd':''}

