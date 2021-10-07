import Selection, FileUtilities, Warnings, QuestionableMath, FileUtilities, MEPUtilities
import sys, os
from pyrevit.coreutils import envvars
from pyrevit import DB, UI, forms
import getpass
import CommandUtils
import Autodesk.Windows
import System.Windows.Media
import System.Windows.Media.Imaging
import System.Diagnostics
import SyncUtility
ribbon = Autodesk.Windows.ComponentManager.Ribbon
import System.Drawing
import clr, sys, datetime, os
from os.path import expanduser
import hashlib
from System import EventHandler, Uri
from threading import Thread
from Autodesk.Revit.UI import TaskDialog
from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from System.Windows.Forms import MessageBox
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException
from pyrevit import script
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

home = expanduser("~")
#creamColor = System.Windows.Media.Color.FromRgb(255, 253, 208)
#roseColor = System.Windows.Media.Color.FromRgb(247, 202, 201)
#fuchsiaColor = System.Windows.Media.Color.FromRgb(255, 0, 255)
#redColor = System.Windows.Media.Color.FromRgb(255, 0, 0)

#uidoc = __revit__.ActiveUIDocument
#doc = __revit__.ActiveUIDocument.Document

#process = System.Diagnostics.Process.GetCurrentProcess()
#print(process)
#process.Kill()

script.set_envvar('IdleTest', "Test")
script.set_envvar('IdleShow', 1)
#script.set_envvar('IdleWindowTimer', 30)
#SyncUtility.SyncandCloseRevit(__revit__, home)
'''
def OnCheckActivityTick(sender, args):
    #print(str(System.DateTime.UtcNow))
    #print("123")
    # ext_event.Raise()
    MessageBox.Show(str(System.DateTime.UtcNow))
    #a = System.DateTime.UtcNow
    #print("123")



inactivityCheckTimer = DispatcherTimer()
inactivityCheckTimer.Tick += EventHandler(OnCheckActivityTick)
inactivityCheckTimer.Interval = TimeSpan(0, 0, 3)
inactivityCheckTimer.Start()
'''



#UI.UIApplication(__revit__.Application).OpenAndActivateDocument(r"C:\Users\mlou\OneDrive - Kohn Pedersen Fox Associates 1\Desktop\KPF_CW_Door_Double.rfa")
'''
print("\n".join(sys.path))

envvars.set_pyrevit_env_var('MINT_CONFIG', {'FAMILY_VIEW_ACTIVATED': False})
print('FAMILY_VIEW_ACTIVATED: ' + str(envvars.get_pyrevit_env_vars()['MINT_CONFIG']['FAMILY_VIEW_ACTIVATED']))


print(getpass.getuser())

#wallOpeningFam = CommandUtils.GetFamily(__revit__.ActiveUIDocument.Document, 'Wall Opening_DD', 'Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa')
#print(wallOpeningFam)
#t = DB.Transaction(__revit__.ActiveUIDocument.Document, 'Test')
#t.Start()
#wallOpeningFam = __revit__.ActiveUIDocument.Document.LoadFamily('Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa', CommandUtils.FamilyOption())
#print(wallOpeningFam)
#t.Commit()



#print(wallOpeningFam)

class MyCustomExternalEventHandler(UI.IExternalEventHandler):
    name = 'MyCustomExternalEventHandler'

    def Execute(self, uiapp):
        wallOpeningFam = CommandUtils.GetFamily(uiapp.ActiveUIDocument.Document, 'Wall Opening_DD',
                                                'Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa')
        uidoc.PostRequestForElementTypePlacement(wallOpeningFam)

    def GetName(self):
        """String identification of the event handler."""
        return self.name

extevent_hndlr = MyCustomExternalEventHandler()
extevent = UI.ExternalEvent.Create(extevent_hndlr)
extevent.Raise()

t = DB.Transaction(doc, 'Test')
t.Start()
doc.Regenerate()
t.Commit()
'''
