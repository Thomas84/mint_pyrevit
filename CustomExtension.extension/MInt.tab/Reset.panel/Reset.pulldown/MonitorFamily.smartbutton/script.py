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

#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'FamilyMonitor'
__context__ = 'zero-doc'

# Set system path

import os
#print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")


config = script.get_config()


# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    # global familyMonitor
    script.set_envvar('FamilyMonitor', True)
    script.toggle_icon(script.set_envvar('FamilyMonitor', True))
    def FamilySizeControl_function(sender, args):
        # global familyMonitor
        if script.get_envvar('FamilyMonitor'):
            size = os.path.getsize(args.FamilyPath + args.FamilyName + ".rfa")
            # UI.TaskDialog.Show(args.FamilyName, str(size))
            result = None
            if size > 5242880:
                result = FamilyCheck.FamilySizeCheckWindow(False).Show()
            else:
                pass
            if result == UI.TaskDialogResult.CommandLink1:
                args.Cancel()
                # args.Dispose()
                UI.UIApplication(args.Document.Application).OpenAndActivateDocument(
                    args.FamilyPath + args.FamilyName + ".rfa")
            elif result == UI.TaskDialogResult.CommandLink2:
                pass
            else:
                pass

    __rvt__.Application.FamilyLoadingIntoDocument += EventHandler[DB.Events.FamilyLoadingIntoDocumentEventArgs](FamilySizeControl_function)
    return True


class ReValueWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        # create pattern maker window and process options
        forms.WPFWindow.__init__(self, xaml_file_name)

    @property
    def word_string(self):
        return self.stringValue_tb.Text

    def select(self, sender, args):
        global key
        self.Close()
        key = self.stringValue_tb.Password

    def string_value_changed(self, sender, args):
        pass

key = "None"

if __name__ == '__main__':
    global key
    hash = "9d7eee23e27d436284560152c36d4b04"
    if script.get_envvar('FamilyMonitor'):
        #password = forms.ask_for_string(title="Please input master password")

        ReValueWindow('PasswordWindow.xaml').show(modal=True)

        salt = "2B9s"
        code = str(key) + salt
        h = hashlib.md5(code.encode())
        if h.hexdigest() == hash:
            state = not script.get_envvar('FamilyMonitor')
            script.set_envvar('FamilyMonitor', state)
            script.toggle_icon(script.get_envvar('FamilyMonitor'))
            TaskDialog.Show("Failed", "Monitoring disabled")
        else:
            TaskDialog.Show("Failed", "Failed to disable monitoring")
    else:
        state = not script.get_envvar('FamilyMonitor')
        script.set_envvar('FamilyMonitor', state)
        script.toggle_icon(script.get_envvar('FamilyMonitor'))