import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'DivHTML'
    # A textblock contains the widget description
    ref = "widgets.paras.DivHTML"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: paras"
    headersection['tomodule','link_ident'] = skicall.makepath('paras')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)

def drop_on_a(skicall):
    "Get the colour dropped, and current colour, and alter divhtml_a accordingly"
    if ('divhtml_a', 'drop') not in skicall.call_data:
        return
    currentcolour = skicall.call_data['divhtml_a', 'drop']
    dropcolour = skicall.call_data.get(('divhtml_b', 'drag'))
    if not dropcolour:
        dropcolour = skicall.call_data.get(('divhtml_c', 'drag'))
    newcolour = _getnewcolour(currentcolour, dropcolour)
    if not newcolour:
        return

    pd = PageData()
    pd['divhtml_a', 'drag'] = newcolour
    pd['divhtml_a', 'drop'] = newcolour
    pd['divhtml_a', 'set_html'] = f"""<p class="w3-{newcolour}">Drop {dropcolour} on {currentcolour} gives {newcolour}</p>"""
    skicall.update(pd)


def drop_on_b(skicall):
    "Get the colour dropped, and current colour, and alter divhtml_b accordingly"
    if ('divhtml_b', 'drop') not in skicall.call_data:
        return
    currentcolour = skicall.call_data['divhtml_b', 'drop']
    dropcolour = skicall.call_data.get(('divhtml_a', 'drag'))
    if not dropcolour:
        dropcolour = skicall.call_data.get(('divhtml_c', 'drag'))
    newcolour = _getnewcolour(currentcolour, dropcolour)
    if not newcolour:
        return

    pd = PageData()
    pd['divhtml_b', 'drag'] = newcolour
    pd['divhtml_b', 'drop'] = newcolour
    pd['divhtml_b', 'set_html'] = f"""<p class="w3-{newcolour}">Drop {dropcolour} on {currentcolour} gives {newcolour}</p>"""
    skicall.update(pd)



def drop_on_c(skicall):
    "Get the colour dropped, and current colour, and alter divhtml_c accordingly"
    if ('divhtml_c', 'drop') not in skicall.call_data:
        return
    currentcolour = skicall.call_data['divhtml_c', 'drop']
    dropcolour = skicall.call_data.get(('divhtml_a', 'drag'))
    if not dropcolour:
        dropcolour = skicall.call_data.get(('divhtml_b', 'drag'))
    newcolour = _getnewcolour(currentcolour, dropcolour)
    if not newcolour:
        return

    pd = PageData()
    pd['divhtml_c', 'drag'] = newcolour
    pd['divhtml_c', 'drop'] = newcolour
    pd['divhtml_c', 'set_html'] = f"""<p class="w3-{newcolour}">Drop {dropcolour} on {currentcolour} gives {newcolour}</p>"""
    skicall.update(pd)



def _getnewcolour(currentcolour, dropcolour):
    "Return a colour depending on the current colour, and the colour dropped into it"
    if currentcolour not in ('red', 'blue', 'purple'):
        return
    if dropcolour not in ('red', 'blue', 'purple'):
        return
    if currentcolour == dropcolour:
        return currentcolour
    if currentcolour != 'purple':
        return 'purple'
    return dropcolour

