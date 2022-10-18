import os

from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Called by a SubmitData responder, and sets up the page"

    # the title and widget decription is in section 'header' which contains a
    # HeadText widget with name 'title' and a TextBlockPara widget with name 'widgetdesc'
    # It also has a ButtonLink2 widget with name 'tomodule'
    headersection = SectionData('header')
    headersection['title', 'large_text'] = 'Angle'
    # A textblock contains the widget description
    ref = "widgets.svgmeters.Angle"
    headersection['widgetdesc','textblock_ref'] = ref
    headersection['widgetdesc','text_refnotfound'] = f'Textblock reference {ref} not found'
    # link to this widgets module page
    headersection['tomodule','button_text'] = "Module: svgmeters"
    headersection['tomodule','link_ident'] = skicall.makepath('svgmeters')
    skicall.update(headersection)

    # this code file contents is placed in section 'codefile' which contains a
    # PreText widget with name 'pretext'
    codesection = SectionData('codefile')
    code = os.path.realpath(__file__)
    with open(code) as f:
        codesection['pretext', 'pre_text'] = f.read()
    skicall.update(codesection)


def reading(skicall):
    "Responds to page update call to submit a new Angle reading"

    try:
        # get the previous measurement, and increment it by 5 degrees
        # ident_data is a string passed with the page update call
        if skicall.ident_data is None:
            measurement = 0
        else:
            measurement = int(skicall.ident_data)
    except:
        raise FailPage(message="Invalid ident_data")

    measurement += 5
    if measurement < 0 or measurement >= 360:
        measurement = 0
    pd = PageData()
    # display the new measurement in the widget
    pd['angle', 'measurement'] = measurement
    # save the measurement as a string in ident_data, which is sent back
    # in the next page update call
    pd.ident_data = str(measurement)
    skicall.update(pd)

    
