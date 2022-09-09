
from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    sd = SectionData('header')
    sd['title', 'large_text'] = 'CheckBox1'
    ref = "widgets.checkbox.CheckBox1"
    sd['widgetdesc','textblock_ref'] = ref
    sd['widgetdesc','text_refnotfound'] = 'Textblock reference %s not found' % ref
    skicall.update(sd)


def respond(skicall):
    "Responds to submission from CheckBox1"

    if ('checkbox1', 'checkbox') not in skicall.call_data:
        raise FailPage(message="No CheckBox1 submission received")

    pd = PageData()

    if skicall.call_data['checkbox1', 'checkbox'] == 'checkbox1set':
        # The checkbox is ticked
        pd['result','para_text'] = "The CheckBox1 is ticked"
    else:
        # The checkbox is not ticked
        pd['result','para_text'] = "The CheckBox1 is not ticked"
        
    skicall.update(pd)
