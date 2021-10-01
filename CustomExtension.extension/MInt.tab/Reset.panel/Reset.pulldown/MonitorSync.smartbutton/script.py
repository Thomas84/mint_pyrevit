import Logger, CommandUtils
import getpass
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from System import Guid
from os.path import expanduser
import ConfigParser, FamilyCheck
import clr, sys, datetime, os
import os.path, hashlib
from pyrevit import HOST_APP, framework
from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework, forms
from System import EventHandler, Uri
from pyrevit.coreutils import envvars
import rpw
import System.Windows.Media
import System.Windows.Media.Imaging
import Autodesk.Windows
ribbon = Autodesk.Windows.ComponentManager.Ribbon
from Autodesk.Revit.UI import TaskDialog
from pyrevit.revit import tabs
import time
from threading import Thread
# noinspection PyUnresolvedReferences
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB import Transaction
# noinspection PyUnresolvedReferences
from Autodesk.Revit.Exceptions import InvalidOperationException


#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'IdleMonitor'
__context__ = 'zero-doc'

# Set system path

import os
#print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")


config = script.get_config()
class SimpleEventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """
    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this
    # Execute method run in Revit API environment.
    def Execute(self, uiapp):
        try:
            self.do_this()
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print("InvalidOperationException catched")
    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"

def delete_elements():
    #time.sleep(12)
    TaskDialog.Show("Trigger Close", "Debug 5")
simple_event_handler = SimpleEventHandler(delete_elements)
# We now need to create the ExternalEvent
ext_event = ExternalEvent.Create(simple_event_handler)
# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    script.set_envvar('IdleMonitor', 0)
    script.set_envvar('IdleCount', 0)

    global window
    def count(sender, args):
        global window
        if script.get_envvar('IdleMonitor') == 1:
            window.show(modal=False)
            script.set_envvar('IdleMonitor', 2)
            args.SetRaiseWithoutDelay()
        elif script.get_envvar('IdleMonitor') == 2:
            i = script.get_envvar('IdleCount')
            if i < 10:
                time.sleep(1)
                script.set_envvar('IdleCount', i + 1)
            else:
                script.set_envvar('IdleMonitor', 3)
                script.set_envvar('IdleCount', 0)
            args.SetRaiseWithoutDelay()
        elif script.get_envvar('IdleMonitor') == 3:
            script.set_envvar('IdleMonitor', 0)
            script.set_envvar('IdleCount', 0)
            TaskDialog.Show("Trigger Close", "Debug")

    def app_start_log(sender, args):
        #global window
        #window = TimerWindow('TimerBox.xaml')
        #TaskDialog.Show("Window Closed", 'AppInti')
        pass

    __rvt__.Idling += EventHandler[UI.Events.IdlingEventArgs](count)
    __rvt__.Application.ApplicationInitialized += EventHandler[DB.Events.ApplicationInitializedEventArgs](app_start_log)
    return True



class TimerWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        # create pattern maker window and process options
        forms.WPFWindow.__init__(self, xaml_file_name)
        self.stringValue_tb.Text = "Revit will close after 10 seconds"

    def word_string(self):
        return self.stringValue_tb.Text

    def wait(self, number):
        time.sleep(number)
        TaskDialog.Show("Trigger Close", "Debug 1")

    def word_set(self, number):
        self.stringValue_tb.Text = str(number)

    def select(self, sender, args):
        script.set_envvar('IdleMonitor', 0)
        script.set_envvar('IdleCount', 0)

        ext_event.Raise()
        self.Hide()

    def string_value_changed(self, sender, args):
        pass

global window
window = TimerWindow(r'..\TimerBox.xaml')

if __name__ == '__main__':
    global window

    #window = TimerWindow('TimerBox.xaml')
    #window.show(modal=False)
    script.set_envvar('IdleMonitor', 1)

    '''
    while i <= 10 and not key:
        window.word_set(i)
        time.sleep(1)
        i += 1

    if key:
        TaskDialog.Show("Window Closed", str(key))
        #window.Close()
    else:
        window.Close()
    '''
