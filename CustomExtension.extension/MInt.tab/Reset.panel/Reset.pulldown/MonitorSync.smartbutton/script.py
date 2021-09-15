import Logger, CommandUtils
import getpass
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from System import Guid
from os.path import expanduser
import ConfigParser
import clr, sys, datetime, os
import os.path
from os import path
from pyrevit import HOST_APP, framework
from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework
from System import EventHandler, Uri
from pyrevit.coreutils import envvars
import rpw
import System.Windows.Media
import System.Windows.Media.Imaging
import Autodesk.Windows

ribbon = Autodesk.Windows.ComponentManager.Ribbon
from Autodesk.Revit.UI import TaskDialog

# from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'Reset'
__context__ = 'zero'

# Set system path

import os

config = script.get_config()


def GetRibbonbyId(id):
    for tab in Autodesk.Windows.ComponentManager.Ribbon.Tabs:
        if tab.Id == id:
            return tab
    return None


# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    # SetUpConfigFile()
    global navigationLock
    navigationLock = False
    global autoSync
    autoSync = False
    global syncTimer
    syncTimer = [120, 90, 60, 30]
    # syncTimer = [4, 3, 2, 1]
    global monitorModels
    monitorModels = {}
    global monitorIdle
    monitorIdle = {}
    global collaborateTab
    collaborateTab = GetRibbonbyId("Collaborate")

    prlxAppAddin = os.getenv('APPDATA') + "\\Autodesk\\Revit\\Addins\\" + \
                   str(__rvt__.Application.VersionNumber) + "\\Prlx.SyncWithCentralTimer.addin"
    prlxProgramAddin = os.getenv('PROGRAMDATA') + "\\Autodesk\\Revit\\Addins\\" + \
                       str(__rvt__.Application.VersionNumber) + "\\Prlx.SyncWithCentralTimer.addin"

    # Logger Setting when start up

    def Check_last_active_time(now):
        interval = 120
        for time in monitorModels:
            if now > time + datetime.timedelta(minutes=interval):
                return True

        return False

    def Idle_sync_function(sender, args):
        global autoSync
        time = datetime.datetime.now()
        if Check_last_active_time(time):
            autoSync = True
        if autoSync:
            TaskDialog.Show("Auto Sync with Central", "Are you still there?")
            autoSync = False
        args.SetRaiseWithoutDelay()

    def document_changed_sync_function(sender, args):
        global navigationLock
        global syncTimer
        time = datetime.datetime.now()
        documentTitle = args.GetDocument().Title
        documentCode = str(args.GetDocument().GetHashCode())

        # lock = CheckSyncTimeConfig(documentTitle, documentCode, time, [4, 3, 2, 1])
        lock = CheckSyncTime(documentTitle, documentCode, time, syncTimer)
        if lock:
            navigationLock = True
        else:
            navigationLock = False
        if args.Document.IsWorkshared and not args.Document.IsLinked and not args.Document.IsFamilyDocument:
            WriteModelChangedTime(documentTitle, documentCode, time)
        # TaskDialog.Show("Lock", str(navigationLock))

    def document_opened_sync_function(sender, args):
        time = datetime.datetime.now()
        documentTitle = args.Document.Title
        documentCode = str(args.Document.GetHashCode())
        # WriteModelOpenTimeConfig(documentTitle, documentCode, time)
        if args.Document.IsWorkshared and not args.Document.IsLinked and not args.Document.IsFamilyDocument:
            WriteModelOpenTime(documentTitle, documentCode, time)

    def document_synced_sync_function(sender, args):
        global navigationLock
        global syncTimer
        time = datetime.datetime.now()
        documentTitle = args.Document.Title
        documentCode = str(args.Document.GetHashCode())
        # WriteModelOpenTimeConfig(documentTitle, documentCode, time)
        if args.Document.IsWorkshared and not args.Document.IsLinked and not args.Document.IsFamilyDocument:
            WriteModelOpenTime(documentTitle, documentCode, time)
            lock = CheckSyncTime(documentTitle, documentCode, time, syncTimer)
            if lock:
                navigationLock = True
            else:
                navigationLock = False

    def view_activated_sync_function(sender, args):
        global navigationLock
        global syncTimer
        time = datetime.datetime.now()
        documentTitle = args.Document.Title
        documentCode = str(args.Document.GetHashCode())
        # TaskDialog.Show(documentTitle, args.Document.GetWorksharingCentralModelPath())
        if args.Document.IsModified:
            lock = CheckSyncTime(documentTitle, documentCode, time, syncTimer)
            if lock:
                navigationLock = True
            else:
                navigationLock = False
        else:
            ChangeRibbonColor(4)
            navigationLock = False
        if args.Document.IsWorkshared and not args.Document.IsLinked and not args.Document.IsFamilyDocument:
            WriteModelChangedTime(documentTitle, documentCode, time)

    def WriteModelOpenTime(model, hashcode, time):
        global monitorModels
        monitorModels[hashcode + "_" + model] = time

    def WriteModelChangedTime(model, hashcode, time):
        global monitorIdle
        monitorIdle[hashcode + "_" + model] = time

    def LocktoCollabToolBar(sender, args):
        global navigationLock
        global monitorModels
        global collaborateTab
        if navigationLock is True:
            collaborateTab.IsActive = True
        else:
            pass

    def CheckSyncTime(model, hashcode, time, deltas):
        global monitorModels
        global collaborateTab
        if hashcode + "_" + model in monitorModels.keys():
            lastSyncedTime = monitorModels[hashcode + "_" + model]
            if lastSyncedTime is not None:
                if time > lastSyncedTime + datetime.timedelta(minutes=deltas[0]):
                    # TaskDialog.Show(model, "1")
                    ChangeRibbonColor(0)
                    collaborateTab.IsActive = True
                    return True
                elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[1]):
                    # TaskDialog.Show(model, "2")
                    ChangeRibbonColor(1)
                    return False
                elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[2]):
                    # TaskDialog.Show(model, "3")
                    ChangeRibbonColor(2)
                    return False
                elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[3]):
                    # TaskDialog.Show(model, "4")
                    ChangeRibbonColor(3)
                    return False
                else:
                    # TaskDialog.Show(model, "5")
                    ChangeRibbonColor(4)
                    return False
            else:
                ChangeRibbonColor(4)
                return False
        else:
            ChangeRibbonColor(4)
            return False

    def ChangeRibbonColor(int):
        colors = []

        defaultColor = System.Windows.Media.Color.FromRgb(238, 238, 238)
        creamColor = System.Windows.Media.Color.FromRgb(255, 253, 208)
        roseColor = System.Windows.Media.Color.FromRgb(247, 202, 201)
        fuchsiaColor = System.Windows.Media.Color.FromRgb(255, 0, 255)
        redColor = System.Windows.Media.Color.FromRgb(255, 0, 0)

        colors.append(redColor)
        colors.append(fuchsiaColor)
        colors.append(roseColor)
        colors.append(creamColor)
        colors.append(defaultColor)
        for tab in ribbon.Tabs:
            for panel in tab.Panels:
                panel.CustomPanelBackground = System.Windows.Media.SolidColorBrush(colors[int])

    # Sync Timer
    if not os.path.isfile(prlxAppAddin) and not os.path.isfile(prlxProgramAddin):
        __rvt__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](
            document_opened_sync_function)
        __rvt__.Application.DocumentSynchronizedWithCentral += EventHandler[
            DB.Events.DocumentSynchronizedWithCentralEventArgs](document_synced_sync_function)
        # __rvt__.Application.DocumentClosed += EventHandler[DB.Events.DocumentClosedEventArgs](document_closed_sync_function)
        Autodesk.Windows.ComponentManager.UIElementActivated += EventHandler[
            Autodesk.Windows.UIElementActivatedEventArgs](LocktoCollabToolBar)
        __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](
            document_changed_sync_function)
        __rvt__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](view_activated_sync_function)
        # __rvt__.Idling += EventHandler[UI.Events.IdlingEventArgs](Idle_sync_function)
    return True


if __name__ == '__main__':
    print('Please do not click this button again.')
