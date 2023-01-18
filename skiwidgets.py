

import os, sys

sys.path.insert(0, "/home/bernard/git/skipole")
sys.path.insert(0, "/home/bernard/git/skilift")

import os

from skipole import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, ServeFile, use_submit_list, skis, PageData, SectionData, set_debug, widget_modules

import modulelist


# the framework needs to know the location of the projectfiles directory holding the project data
# and static files.

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))
PROJECT = "skiwidgets"

# set tuple of module names into proj_data

PROJ_DATA={ 'modules': widget_modules()
          }

def start_call(called_ident, skicall):
    "Call modulelist.handle_page_not_found if no page found, otherwise return the called_ident"
    if called_ident is None:
        return modulelist.handle_page_not_found(skicall)
    return called_ident

@use_submit_list
def submit_data(skicall):
    """The use_submit_list decorator redirects calls to othe packages, modules and functions"""
    raise ServerError(message=f"Responder {skicall.ident_list[-1]} does not have a correct submit list set")

def end_call(page_ident, page_type, skicall):
    """This function is called prior to returning a page,
       it can also be used to return an optional session cookie string."""
    return

# create the wsgi application
application = WSGIApplication(project=PROJECT,
                              projectfiles=PROJECTFILES,
                              proj_data=PROJ_DATA,
                              start_call=start_call,
                              submit_data=submit_data,
                              end_call=end_call,
                              url="/skiwidgets")


# Add the 'skis' application which serves javascript and css files required by
# the framework widgets.

skis_application = skis.makeapp()
application.add_project(skis_application, url='/skiwidgets/lib')

# The above shows the main application served at "/skiwidgets" and the skis library
# project served at "/skiwidgets/lib"

if __name__ == "__main__":

    set_debug(True)
    host = "127.0.0.1"
    # host = "0.0.0.0"
    port = 8000

    from skilift import make_skiadmin, development_server

    skiadmin_application = make_skiadmin(editedprojname=PROJECT, examples="http://www.webparametrics.co.uk/skiwidgets/")
    application.add_project(skiadmin_application, url='/skiwidgets/skiadmin')

    # if using the development server from skilift
    print("Serving %s on port %s. Call http://localhost:%s/skiwidgets/skiadmin to edit." % (PROJECT, port, port))
    development_server(host, port, application)


    # if using the waitress server
    #from waitress import serve
    #serve(application, host=host, port=port, max_request_body_size=1000)

    # note:
    # max_request_body_size has been set to 1000, as this site illustrates widgets only
    # and the upload file widgets could be used to send something very large unless limited

