
from skipole import FailPage, GoTo, ValidateError, ServerError, ServeFile, PageData, SectionData

from skipole.skilift import editwidget



def retrieve_module_list(skicall):
    "this call is to retrieve data for listing widget modules"

    # table of widget modules

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    contents = []

    modules_tuple = editwidget.widget_modules()

    for name in modules_tuple:
        ref = 'widgets.' + name + '.module'
        notfound = 'Textblock reference %s not found' % ref
        contents.append([name, name, '', ref, notfound, ''])

    pd = PageData()
    pd["modules","link_table"] = contents

    skicall.update(pd)


def retrieve_widgets_list(skicall):
    "this call is to retrieve data for listing widgets in a module"

    call_data = skicall.call_data

    if 'module' in call_data:
        module_name = call_data['module']
    else:
        raise FailPage("Module not identified")

    modules_tuple = editwidget.widget_modules()

    if module_name not in modules_tuple:
        raise FailPage("Module not identified")

    # set module into call_data
    call_data['module'] = module_name
    call_data['headtext'] = module_name

    pd = PageData()
    pd['title', 'large_text'] = "Module: " + module_name
    ref = 'widgets.' + module_name + '.module'
    pd['moduledesc','textblock_ref'] = ref
    pd['moduledesc','text_refnotfound'] = f'Textblock reference {ref} not found'

    # table of widgets

    # col 0 is the visible text to place in the link,
    # col 1 is the get field of the link
    # col 2 is the get field of the link
    # col 3 is the reference string of a textblock to appear in the column adjacent to the link
    # col 4 is text to appear if the reference cannot be found in the database
    # col 5 normally empty string, if set to text it will replace the textblock

    widget_list = editwidget.widgets_in_module(module_name)
    contents = []
    for widget in widget_list:
        widgetref = ".".join(("widgets", module_name, widget.classname))
        notfound = f'Textblock reference {widgetref} not found'
        classname = widget.classname
        contents.append([classname, classname, module_name, widgetref, notfound, ''])

    pd["widgets","link_table"] = contents
    skicall.update(pd)


def retrieve_widgets_edit(skicall):
    "Set the target page which shows the widget"

    if 'module' not in skicall.call_data:
        raise FailPage("Module not identified")

    if 'widget' not in skicall.call_data:
        raise FailPage("Widget not identified")

    module_name = skicall.call_data['module']
    widget_name = skicall.call_data['widget']

    if (not module_name) or (not widget_name):
        raise FailPage("Invalid call")

    modules_tuple = editwidget.widget_modules()

    if module_name not in modules_tuple:
        raise FailPage("Module not identified")

    widget_list = [ widget.classname for widget in editwidget.widgets_in_module(module_name) ]
    if widget_name not in widget_list:
        raise FailPage("Widget not identified")

    targetpath = skicall.makepath(module_name, widget_name)

    raise GoTo(targetpath)




