from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    sd = SectionData('header')
    sd['title', 'large_text'] = 'ShowCallData'
    ref = "widgets.debug_tools.ShowCallData"
    sd['widgetdesc','textblock_ref'] = ref
    sd['widgetdesc','text_refnotfound'] = 'Textblock reference %s not found' % ref
    skicall.update(sd)

    if ('setcalldata', 'input_text') in skicall.call_data:
        pd = PageData()
        pd['setcalldata', 'input_text'] = skicall.call_data['setcalldata', 'input_text']
        skicall.update(pd)



