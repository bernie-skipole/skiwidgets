import os, json

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

# Normally table data would be taken from a file or database or other source of data.
TABLECOL1 = [10, 100, 1000, 10000]
TABLECOL2 = [2, 20, 200, 2000]
TABLEINPUT = {'aaa':5, 'bbb':50, 'ccc':500, 'ddd':5000}
KEYS = list(TABLEINPUT.keys())


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

    # illustrate the table by filling in initial global values
    pd = PageData()
    pd['inputtable3','up_getfield1'] = KEYS
    pd['inputtable3','down_getfield1'] = KEYS
    pd['inputtable3','col1'] = TABLECOL1
    pd['inputtable3','col2'] = TABLECOL2

    if 'tabledone' not in skicall.call_data:
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
    # the submission, and this ensures they are all present, it returns a
    # dictionary of all the keys with empty values

    return { key:'' for key in KEYS}


def renew(skicall):
    """Renews the table on inputdict being received"""
    if ('inputtable3', 'inputdict') not in skicall.call_data:
        raise FailPage(message="No submission received")
    try:
        inputdict = skicall.call_data['inputtable3', 'inputdict']
        pd = PageData()
        valuedict = {key:int(inputdict[key]) for key in KEYS}
        pd['inputtable3', 'inputdict'] = valuedict
        stylelist = _set_limit_colours(valuedict)
        if stylelist:
            pd['inputtable3','cell_style'] = stylelist
        skicall.update(pd)
    except:
        raise FailPage(message="Invalid submission received")
    # now call index(skicall) to fill in the page again, but flag data is present
    skicall.call_data['tabledone'] = True
    index(skicall)


def _set_limit_colours(valuedict):
    "Returns a style list, setting cell colours if max or min value has been reached"
    # stylelist is a list of lists, each being [row, col, cssstyle] with row, col
    # being the table body row and column (starting at 1 rather than zero).
    # In this example, colours are set if minimum, or maximum values have
    # been reached
    stylelist = []
    for row, key in enumerate(KEYS):
        if key not in valuedict:
            continue
        value = valuedict[key]
        # maximums
        if value == TABLECOL1[row]:
            stylelist.append([row+1, 1, 'background-color:Yellow;color:Black;'])
        elif value > TABLECOL1[row]:
            stylelist.append([row+1, 1, 'background-color:Red;color:Yellow;'])
        else:
           stylelist.append([row+1, 1, ''])
        # minimums
        if value == TABLECOL2[row]:
            stylelist.append([row+1, 2, 'background-color:Yellow;color:Black;'])
        elif value < TABLECOL2[row]:
            stylelist.append([row+1, 2, 'background-color:Red;color:Yellow;'])
        else:
           stylelist.append([row+1, 2, ''])
    return stylelist


def up(skicall):
    """Up arrow received, increment value, returns JSON update"""
    if ('inputtable3','up_getfield1') not in skicall.call_data:
        raise FailPage(message="No submission received")
    if ('inputtable3','getfield3') not in skicall.call_data:
        raise FailPage(message="No submission received")
    try:
        key = skicall.call_data['inputtable3','up_getfield1']
        value = int(skicall.call_data['inputtable3','getfield3'])
        if key == 'aaa':
            inputdict = { key:value+1 }
        elif key == 'bbb':
             inputdict = { key:value+10 }
        elif key == 'ccc':
             inputdict = { key:value+100 }
        elif key == 'ddd':
            inputdict = { key:value+1000 }
        else:
            raise FailPage(message="Invalid submission received")
        pd = PageData()
        stylelist = _set_limit_colours(inputdict)
        if stylelist:
            pd['inputtable3','cell_style'] = stylelist
        pd['inputtable3', 'inputdict'] = inputdict
        skicall.update(pd)
    except:
        raise FailPage(message="Invalid submission received")


def down(skicall):
    """Down arrow received, decrement value, returns JSON update"""
    if ('inputtable3','down_getfield1') not in skicall.call_data:
        raise FailPage(message="No submission received")
    if ('inputtable3','getfield3') not in skicall.call_data:
        raise FailPage(message="No submission received")
    try:
        key = skicall.call_data['inputtable3','down_getfield1']
        value = int(skicall.call_data['inputtable3','getfield3'])
        if key == 'aaa':
            inputdict = { key:value-1 }
        elif key == 'bbb':
             inputdict = { key:value-10 }
        elif key == 'ccc':
             inputdict = { key:value-100 }
        elif key == 'ddd':
            inputdict = { key:value-1000 }
        else:
            raise FailPage(message="Invalid submission received")
        pd = PageData()
        stylelist = _set_limit_colours(inputdict)
        if stylelist:
            pd['inputtable3','cell_style'] = stylelist
        pd['inputtable3', 'inputdict'] = inputdict
        skicall.update(pd)
    except:
        raise FailPage(message="Invalid submission received")
