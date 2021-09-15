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

config = script.get_config()


def test_function(sender, args):
    print("test")


def GetRibbonbyId(id):
    for tab in Autodesk.Windows.ComponentManager.Ribbon.Tabs:
        if tab.Id == id:
            return tab
    return None

# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):

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
                  ";_App_Closed; _Version:" + __rvt__.Application.VersionName + \
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

    def model_closing_log(sender, args):
        global appLogger
        docTitle = args.Document.Title
        message = str(datetime.datetime.now()) + \
                  ";_Closed_Document; Document:" + docTitle + \
                  "\n"
        try:
            appLogger.Log(message, user)
        except:
            pass


    # Command Overwrite
    wallOpeningUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.WallOpening,
                                                      CommandUtils.WallOpeningReplacement)
    importCADUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.ImportCAD,
                                                    CommandUtils.ImportReplacement)
    modelInPlaceUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.ModelInPlace,
                                                    CommandUtils.ModelInPlaceReplacement)
    hideInViewUtil = CommandUtils.CommandReplacement(__rvt__, UI.PostableCommand.HideElements,
                                                    CommandUtils.HideElementReplacement)
    #TODO reminder for classification ？？？ after view activated pick view_use or pick view template
    #TODO： Uncheck Anlytical
    # Revit Log
    __rvt__.Application.ApplicationInitialized += EventHandler[DB.Events.ApplicationInitializedEventArgs](app_start_log)
    __rvt__.ApplicationClosing += EventHandler[UI.Events.ApplicationClosingEventArgs](app_shutdown_log)
    __rvt__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](model_open_log)
    __rvt__.Application.DocumentClosing += EventHandler[DB.Events.DocumentClosingEventArgs](model_closing_log)
    __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](log_function)


if __name__ == '__main__':
    print('Please do not click this button again.')