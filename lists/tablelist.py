import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


# TABLECONTENTS is a global variable, normally data would be taken from a database
TABLECONTENTS = ['one', 'two', 'three', 'four']


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'TableList'
    # A textblock contains the widget description
    ref = "widgets.lists.TableList"
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

    # fill in the TableList widget with initial values, in this case the items are
    # taken from TABLECONTENTS, and the get fields describe the row chosen, and the table layout
    # as a series of indeces of TABLECONTENTS
    pd = PageData()
    pd['tablelist','contents'] = [ [TABLECONTENTS[0], "0_0_1_2_3", "0_0_1_2_3", "0_0_1_2_3"],
                                   [TABLECONTENTS[1], "1_0_1_2_3", "1_0_1_2_3", "1_0_1_2_3"],
                                   [TABLECONTENTS[2], "2_0_1_2_3", "2_0_1_2_3", "2_0_1_2_3"],
                                   [TABLECONTENTS[3], "3_0_1_2_3", "3_0_1_2_3", "3_0_1_2_3"]
                                 ]
    skicall.update(pd)


def up(skicall):
    "Called to Move the row upwards"
    if ('tablelist', 'contents') not in skicall.call_data:
        raise FailPage(message="No submission received")

    index(skicall)
    try:
        rowlist = list( int(i) for i in skicall.call_data['tablelist', 'contents'].split('_') )
        # get the row of the table chosen
        row = rowlist[0]
        if not row:
            # row position is 0, cannot move above row 0
            return
        # get the table layout
        table = rowlist[1:]
        itemtomove = table[row]
        table.remove(itemtomove)
        table.insert(row-1, itemtomove)
    except:
        raise FailPage(message="Invalid submission received")

    tablestring = "_".join(str(i) for i in table)
    contents = []
    for rownumber, item in enumerate(table):
        rowstring = str(rownumber) + "_" + tablestring
        rowlist = [TABLECONTENTS[item], rowstring, rowstring, rowstring]
        contents.append(rowlist)
    pd = PageData()
    pd['tablelist','contents'] = contents
    skicall.update(pd)




