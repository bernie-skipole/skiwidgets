import os, json

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


# In this example, TABLECONTENTS is a global variable, normally data would be
# taken from a file or database or other source of data.
TABLECONTENTS = ['apple', 'pear', 'banana', 'strawberry']


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

    # fill in the TableList widget with initial values, in this case the list items
    # are taken from TABLECONTENTS, and the get fields for up, down, remove are the
    # row number of the button pressed
    pd = PageData()
    pd['tablelist','contents'] = [ [TABLECONTENTS[0], "0", "0", "0"],
                                   [TABLECONTENTS[1], "1", "1", "1"],
                                   [TABLECONTENTS[2], "2", "2", "2"],
                                   [TABLECONTENTS[3], "3", "3", "3"]
                                 ]

    # Normally the list would be altered on the source of the data, such as a database.
    # In this example the list is set onto the client browser, using the ident_data
    # attribute of pd. The client browser will send this list back when a widget
    # submits data and it will be available as the skicall.ident_data attribute. So
    # the list is persistent to the client session.
    # As ident_data must be a string, this example uses json.dumps to serialise a
    # list of indexes to the TABLECONTENTS list, rather than the full list itself.
    pd.ident_data = json.dumps([0,1,2,3])
    skicall.update(pd)


def _createtablecontents(skicall, indexlist):
    """Takes a list of index numbers, such as [0,1,2,3], these numbers
       being indexes of the TABLECONTENTS list, and creates the new table
       contents, then updates skicall"""
    if not indexlist:
        pd = PageData()
        pd['tablelist','contents'] = []
        pd['tablelist','hide'] = True
        pd.ident_data = "[]"
        skicall.update(pd)
        return

    contents = []
    for rownumber, itemindex in enumerate(indexlist):
        rowstring = str(rownumber)
        rowlist = [TABLECONTENTS[itemindex], rowstring, rowstring, rowstring]
        contents.append(rowlist)
    pd = PageData()
    pd['tablelist','contents'] = contents
    pd.ident_data = json.dumps(indexlist)
    skicall.update(pd)


def up(skicall):
    "Called to move the row upwards"
    # the get field of the button pressed is in skicall.call_data
    if ('tablelist', 'contents') not in skicall.call_data:
        raise FailPage(message="No submission received")
    if skicall.ident_data is None:
        # no table data has been received
        raise FailPage(message="Invalid submission received")

    index(skicall)
    try:
        # get the row of the table from the button pressed
        row = int(skicall.call_data['tablelist', 'contents'])
        if not row:
            # row position is 0, cannot move above row 0
            return

        indexlist = json.loads(skicall.ident_data)
        # indexlist is a list such as [0,1,2,3] giving the order of
        # the indexes of the TABLECONTENTS list

        # move the selected row in the indexlist
        itemtomove = indexlist[row]
        indexlist.remove(itemtomove)
        indexlist.insert(row-1, itemtomove)
    except:
        raise FailPage(message="Invalid submission received")

    # update the table using the new indexlist
    _createtablecontents(skicall, indexlist)



def down(skicall):
    "Called to move the row downwards"
    # the get field of the button pressed is in skicall.call_data
    if ('tablelist', 'contents') not in skicall.call_data:
        raise FailPage(message="No submission received")
    if skicall.ident_data is None:
        # no table data has been received
        raise FailPage(message="Invalid submission received")

    index(skicall)
    try:
        # get the row of the table from the button pressed
        row = int(skicall.call_data['tablelist', 'contents'])

        indexlist = json.loads(skicall.ident_data)
        # indexlist is a list such as [0,1,2,3] giving the order of
        # the indexes of the TABLECONTENTS list

        if row >= len(indexlist) - 1:
            # row is at the last position, cannot move further down
            return

        # move the selected row in the indexlist
        itemtomove = indexlist[row]
        indexlist.remove(itemtomove)
        indexlist.insert(row+1, itemtomove)
    except:
        raise FailPage(message="Invalid submission received")

    # update the table using the new indexlist
    _createtablecontents(skicall, indexlist)



def remove(skicall):
    "Called to remove a row"
    # the get field of the button pressed is in skicall.call_data
    if ('tablelist', 'contents') not in skicall.call_data:
        raise FailPage(message="No submission received")
    if skicall.ident_data is None:
        # no table data has been received
        raise FailPage(message="Invalid submission received")

    index(skicall)
    try:
        # get the row of the table from the button pressed
        row = int(skicall.call_data['tablelist', 'contents'])

        indexlist = json.loads(skicall.ident_data)
        # indexlist is a list such as [0,1,2,3] giving the order of
        # the indexes of the TABLECONTENTS list

        # remove the selected row in the indexlist
        itemtoremove = indexlist[row]
        indexlist.remove(itemtoremove)
    except:
        raise FailPage(message="Invalid submission received")

    # update the table using the new indexlist
    _createtablecontents(skicall, indexlist)




