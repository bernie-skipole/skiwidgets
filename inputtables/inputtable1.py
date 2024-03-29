import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

# Normally table data would be taken from a file or database or other source of data.
TABLECOL1 = ["1 one", "1 two", "1 three", "1 four"]
TABLECOL2 = ["2 one", "2 two", "2 three", "2 four"]
TABLEINPUT = {'aaa':'input1', 'bbb':'input2', 'ccc':'input3', 'ddd':'input4'}
KEYS = list(TABLEINPUT.keys())

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
    pd['inputtable1','col2'] = TABLECOL2

    # col1 is updated with submitted values if they have been received
    if ('inputtable1', 'inputdict') not in skicall.call_data:
        # on the first call to this page ('inputtable1', 'inputdict') will
        # not be in skicall.call_data, so col1 and inputdict are set with initial values
        pd['inputtable1','col1'] = TABLECOL1
        pd['inputtable1', 'inputdict'] = TABLEINPUT
    else:
        # however, after data submission, call_data will be defined, so update col1
        # and inputdict with the values received
        call_data = skicall.call_data['inputtable1', 'inputdict']
        # note, listing received data by order of key in KEYS ensures
        # the list is kept in the right order
        pd['inputtable1', 'col1'] = list(call_data[key] for key in KEYS)
        pd['inputtable1', 'inputdict'] = {key:call_data[key] for key in KEYS}

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

    return { key:'' for key in KEYS}


def test(skicall):
    """Chooses which test to run, depending on button pressed.
       A FieldStoreSubmit responder checks for the get_field1 field
       and stores the received data in skicall.submit_dict['received'].
       The responder has general_json as its target
       so the PageData values set here are sent as a JSON call"""
    if 'received' not in skicall.submit_dict:
        return
    receiveddict = skicall.submit_dict['received']
    if receiveddict.get(('test1', 'get_field1')) == 'test1':
        _test1(skicall)
    elif receiveddict.get(('test2', 'get_field1')) == 'test2':
        _test2(skicall)
    elif receiveddict.get(('test3', 'get_field1')) == 'test3':
        _test3(skicall)


def _test1(skicall):
    "Places string 'test1' into the third input field"
    pd = PageData()
    pd['inputtable1','inputdict'] = {'ccc':'test1'}
    skicall.update(pd)


def _test2(skicall):
    "Places style strings into two table cells"
    pd = PageData()
    pd['inputtable1','cell_style'] = [[1,1,"background-color:Red;color:Yellow;"], [2,2,"background-color:Yellow;color:Black;"]]
    skicall.update(pd)


def _test3(skicall):
    "Places new data into column 2"
    pd = PageData()
    pd['inputtable1','col2'] = ["col2 row1 test3", "col2 row2 test3", "col2 row3 test3", "col2 row4 test3"]
    skicall.update(pd)
