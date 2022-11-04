

import os

########### uses development version of skipole###
#import sys
#sys.path.insert(0, "/home/bernard/git/skipole")
##################################################

from skipole import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, ServeFile, use_submit_list, skis, PageData, SectionData

# get editwidget to find module names, and development_server if not running waitress
from skipole.skilift import editwidget, development_server

import modulelist


# the framework needs to know the location of the projectfiles directory holding the project data
# and static files.

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))
PROJECT = "skiwidgets"

# set tuple of module names into proj_data

PROJ_DATA={ 'modules': editwidget.widget_modules()
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

    # If called as a script, this portion runs the python waitress server
    # and serves the project.

    ###############################################################################
    #
    # you could add the 'skiadmin' sub project
    # which can be used to develop pages for your project
    #
    ############################### THESE LINES ADD SKIADMIN ######################
    #                                                                             
    from skipole import skiadmin                                                  
    skiadmin_application = skiadmin.makeapp(editedprojname=PROJECT, examples="/skiwidgets/")
    application.add_project(skiadmin_application, url='/skiwidgets/skiadmin')     
    #                                                                             
    ###############################################################################

    from skipole import set_debug
    set_debug(True) 

    # if using the waitress server
    # from waitress import serve

    # serve the application, note host 0.0.0.0 rather than
    # 127.0.0.1 - so this will be available externally

    # host = "0.0.0.0"
    host = "127.0.0.1"
    port = 8000

    # using waitress
    # serve(application, host=host, port=port, max_request_body_size=1000)

    # waitress serve arguments
    #
    # max_request_body_size has been set to 1000, as this site illustrates widgets only
    # and the upload file widgets could be used to send something very large unless limited

    # or skilift development server
    print(f"Serving {PROJECT} on port {port}")
    development_server(host, port, application)



