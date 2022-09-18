
from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    sd = SectionData('header')
    sd['title', 'large_text'] = 'DropDown1'
    ref = "widgets.dropdown.DropDown1"
    sd['widgetdesc','textblock_ref'] = ref
    sd['widgetdesc','text_refnotfound'] = 'Textblock reference %s not found' % ref
    skicall.update(sd)

    pd = PageData()
    pd['dropdown1', 'option_list'] = ["One", "Two", "Three", "Four"]
    pd['dropdown1', 'selectvalue'] = "Two"
    skicall.update(pd)


def respond(skicall):
    "Responds to submission from DropDown1"

    if ('dropdown1', 'selectvalue') not in skicall.call_data:
        raise FailPage(message="No DropDown1 submission received")

 
