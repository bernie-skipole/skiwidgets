from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData


def index(skicall):
    "Sets up the page"

    sd = SectionData('header')
    sd['title', 'large_text'] = 'ConfirmBox1'
    ref = "widgets.confirm.ConfirmBox1"
    sd['widgetdesc','textblock_ref'] = ref
    sd['widgetdesc','text_refnotfound'] = 'Textblock reference %s not found' % ref
    skicall.update(sd)



def show_widget(skicall):
    "Called by a button to show the checkbox"
    if ('buttonlink2', 'get_field1') not in skicall.call_data:
       raise FailPage(message="Invalid call")

    if skicall.call_data['buttonlink2', 'get_field1'] != 'show':
      raise FailPage(message="Invalid call")

    pd = PageData()
    pd['confirmbox1', 'hide'] = False

    skicall.update(pd)


def cancel(skicall):
    "Responds to cancel submission from confirmbox1"

    pd = PageData()
    pd['confirmbox1', 'hide'] = True

    pd['result', 'para_text'] = "The operation has been cancelled"
        
    skicall.update(pd)


def confirm(skicall):
    "Responds to confirm submission from confirmbox1"

    pd = PageData()
    pd['confirmbox1', 'hide'] = True

    pd['result', 'para_text'] = "The operation has been confirmed"
        
    skicall.update(pd)
