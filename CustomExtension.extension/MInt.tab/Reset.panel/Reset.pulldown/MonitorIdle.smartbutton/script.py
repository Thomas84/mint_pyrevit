from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework, forms
import Autodesk.Windows
ribbon = Autodesk.Windows.ComponentManager.Ribbon
import time
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException
from System import EventHandler, Uri
from threading import Thread
from Autodesk.Revit.UI import TaskDialog
from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from System.Windows.Forms import MessageBox
import clr, sys, datetime, os
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException
import rpw
from pyrevit.forms import WPFWindow
from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent, TaskDialog
from System import EventHandler, Uri
from pyrevit import script
import SyncUtility
from os.path import expanduser
import os
#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'IdleMonitor'
__context__ = 'zero-doc'
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc
home = expanduser("~")
__persistentengine__ = True

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    pass
if __name__ == '__main__':
    print(script.get_envvar('LastActiveTime') + datetime.timedelta(minutes=1))
    print(script.get_envvar('IdleTrigger'))
    print(script.get_envvar('IdleShow') == 1 and (datetime.datetime.now() > script.get_envvar('LastActiveTime') + datetime.timedelta(minutes=180) or script.get_envvar('IdleTrigger') == 1))