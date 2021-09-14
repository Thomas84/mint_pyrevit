import Logger, CommandUtils
import getpass
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from System import Guid
from os.path import expanduser
import ConfigParser
import clr,sys, datetime, os
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

#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'Reset'
__context__ = 'zero'

# Set system path

import os
#print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")


config = script.get_config()


def test_function(sender, args):
    print("test")

'''
# do the even stuff here
def SetUpConfigFile():

    home = expanduser("~")
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings
    try:
        Config.add_section('NavisFilePath')
        Config.set('NavisFilePath', 'DataPath', ' ')
        Config.add_section('OpenModels')
        # Add master new system folder setting
        Config.add_section('OpenModels')
    except:
        pass
    cfgfile = open(home + "\\MintTools.ini", 'w')
    Config.write(cfgfile)
'''

def GetRibbonbyId(id):
    for tab in Autodesk.Windows.ComponentManager.Ribbon.Tabs:
        if tab.Id == id:
            return tab
    return None

# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    #SetUpConfigFile()
    global navigationLock
    navigationLock = False
    global syncTimer
    syncTimer = [120, 90, 60, 30]
    #syncTimer = [4, 3, 2, 1]
    global monitorModels
    monitorModels = {}
    global collaborateTab
    collaborateTab = GetRibbonbyId("Collaborate")

    prlxAppAddin = os.getenv('APPDATA') + "\\Autodesk\\Revit\\Addins\\" + \
        str(__rvt__.Application.VersionNumber) + "\\Prlx.SyncWithCentralTimer.addin"
    prlxProgramAddin = os.getenv('PROGRAMDATA') + "\\Autodesk\\Revit\\Addins\\" + \
        str(__rvt__.Application.VersionNumber) + "\\Prlx.SyncWithCentralTimer.addin"


    # Logger Setting when start up
    global logger
    home = os.getenv('USERPROFILE')
    user = getpass.getuser()
    cloudLogLocation = "\\\\kpf.com\\corporate\\Zdrive\\0002_03_BIM\\05_Research\\Log-Files\\Mint\\"
    d = datetime.datetime.now()
    localPath = home + "\\" + str(d.year) + "_" + \
                str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLog.txt"

    serverPath = cloudLogLocation + user + "\\" + str(d.year) + "_" + \
                 str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLog.txt"
    if os.path.exists(cloudLogLocation):
        logger = Logger.MintLogger(serverPath)

    else:
        logger = Logger.MintLogger(localPath)

    # Logger Setting when start up
    global appLogger
    home = os.getenv('USERPROFILE')
    user = getpass.getuser()
    cloudAppLogLocation = "\\\\kpf.com\\corporate\\Zdrive\\0002_03_BIM\\05_Research\\Log-Files\\App\\"
    d = datetime.datetime.now()
    localAppPath = home + "\\" + str(d.year) + "_" + \
                str(d.month) + "_" + str(d.day) + "_" + user + "_RevitAppLog.txt"

    serverAppPath = cloudAppLogLocation + user + "\\" + str(d.year) + "_" + \
                 str(d.month) + "_" + str(d.day) + "_" + user + "_RevitAppLog.txt"
    if os.path.exists(cloudAppLogLocation):
        appLogger = Logger.MintLogger(serverAppPath)

    else:
        appLogger = Logger.MintLogger(localAppPath)

    def log_function(sender, args):
        global logger
        separator = ","
        docTitle = args.GetDocument().Title
        message = str(datetime.datetime.now()) + \
                  ";_Title:" + docTitle + \
                  ";_Transactions:" + separator.join(args.GetTransactionNames()) + \
                  ";_Added:" + separator.join(str(ele.IntegerValue) for ele in args.GetAddedElementIds()) + \
                  ";_Deleted:" + separator.join(str(ele.IntegerValue) for ele in args.GetDeletedElementIds()) + \
                  ";_Modified:" + separator.join(str(ele.IntegerValue) for ele in args.GetModifiedElementIds()) + \
                  "\n"
        try:
            logger.Log(message, user)
        except:
            pass

    def app_start_log(sender, args):
        global appLogger
        message = str(datetime.datetime.now()) + \
                  ";_App_Start; _Version:" + __rvt__.Application.VersionName + \
                  "\n"
        try:
            appLogger.Log(message, user)
        except:
            pass

    def app_shutdown_log(sender, args):
        global appLogger
        message = str(datetime.datetime.now()) + \
                  ";_App_Start; _Version:" + __rvt__.Application.VersionName + \
                  "\n"
        try:
            appLogger.Log(message, user)
        except:
            pass

    def model_open_log(sender, args):
        global appLogger
        docTitle = args.Document.Title
        message = str(datetime.datetime.now()) + \
                  ";_Opened_Document; Document:" + docTitle + \
                  "\n"
        try:
            appLogger.Log(message, user)
        except:
            pass

    def document_changed_sync_function(sender, args):
        global navigationLock
        global syncTimer
        time = datetime.datetime.now()
        documentTitle = args.GetDocument().Title
        documentCode = str(args.GetDocument().GetHashCode())

        #lock = CheckSyncTimeConfig(documentTitle, documentCode, time, [4, 3, 2, 1])
        lock = CheckSyncTime(documentTitle, documentCode, time, syncTimer)
        if lock:
            navigationLock = True
        else:
            navigationLock = False
        #TaskDialog.Show("Lock", str(navigationLock))


    def document_opened_sync_function(sender, args):
        time = datetime.datetime.now()
        documentTitle = args.Document.Title
        documentCode = str(args.Document.GetHashCode())
        #WriteModelOpenTimeConfig(documentTitle, documentCode, time)
        if args.Document.IsWorkshared and not args.Document.IsLinked and not args.Document.IsFamilyDocument:
            WriteModelOpenTime(documentTitle, documentCode, time)


    def document_synced_sync_function(sender, args):
        global navigationLock
        global syncTimer
        time = datetime.datetime.now()
        documentTitle = args.Document.Title
        documentCode = str(args.Document.GetHashCode())
        #WriteModelOpenTimeConfig(documentTitle, documentCode, time)
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
        #TaskDialog.Show(documentTitle, args.Document.GetWorksharingCentralModelPath())
        if args.Document.IsModified:
            lock = CheckSyncTime(documentTitle, documentCode, time, syncTimer)
            if lock:
                navigationLock = True
            else:
                navigationLock = False
        else:
            ChangeRibbonColor(4)
            navigationLock = False


    def WriteModelOpenTime(model, hashcode, time):
        global monitorModels
        monitorModels[hashcode + "_" + model] = time


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

    # Command Overwrite
    wallOpeningUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.WallOpening,
                                                      CommandUtils.WallOpeningReplacement)
    importCADUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.ImportCAD,
                                                    CommandUtils.ImportReplacement)
    modelInPlaceUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.ModelInPlace,
                                                    CommandUtils.ModelInPlaceReplacement)
    hideInViewUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.HideElements,
                                                    CommandUtils.HideElementReplacement)

    # Revit Log
    __rvt__.Application.ApplicationInitialized += EventHandler[DB.Events.ApplicationInitializedEventArgs](app_start_log)
    __rvt__.ApplicationClosing += EventHandler[UI.Events.ApplicationClosingEventArgs](app_shutdown_log)
    __rvt__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](model_open_log)
    __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](log_function)

    # Sync Timer
    if not os.path.isfile(prlxAppAddin) and not os.path.isfile(prlxProgramAddin):
        __rvt__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](document_opened_sync_function)
        __rvt__.Application.DocumentSynchronizedWithCentral += EventHandler[DB.Events.DocumentSynchronizedWithCentralEventArgs](document_synced_sync_function)
        #__rvt__.Application.DocumentClosed += EventHandler[DB.Events.DocumentClosedEventArgs](document_closed_sync_function)
        Autodesk.Windows.ComponentManager.UIElementActivated += EventHandler[Autodesk.Windows.UIElementActivatedEventArgs](LocktoCollabToolBar)
        __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](document_changed_sync_function)
        __rvt__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](view_activated_sync_function)
    return True

if __name__ == '__main__':
    print('Please do not click this button again.')