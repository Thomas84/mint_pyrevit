import Logger, CommandUtils
import getpass
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from System import Guid
from os.path import expanduser
import ConfigParser, FamilyCheck
import clr, sys, datetime, os
import os.path, hashlib
from os import path
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


#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'IdleMonitor'
__context__ = 'zero-doc'

# Set system path

import os
#print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")


config = script.get_config()

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

    def word_set(self, number):
        self.stringValue_tb.Text = str(number)

    def select(self, sender, args):
        script.set_envvar('IdleMonitor', 0)
        script.set_envvar('IdleCount', 0)
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
