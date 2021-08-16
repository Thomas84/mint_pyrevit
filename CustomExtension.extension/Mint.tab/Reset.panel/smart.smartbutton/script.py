import Logger, CommandUtils
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

#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'Reset'
__context__ = 'zero'

# Set system path

import os
print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")


config = script.get_config()


def test_function(sender, args):
    print("test")

# do the even stuff here

def log_function(sender, args):
    home = os.getenv('USERPROFILE')

    user = __revit__.Application.Username
    cloudLogLocation = "C:\\Users\\mengf\\Desktop\\Log\\"
    d = datetime.datetime.now()
    localPath = home + "\\" + str(d.year) + "_" + \
                str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLlog.txt"

    serverPath = cloudLogLocation + user + "\\" + str(d.year) + "_" + \
                 str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLog.txt"

    localLogger = Logger.MintLogger(localPath)
    cloudLogger = Logger.MintLogger(serverPath)

    separator = ","
    docTitle = args.GetDocument().Title
    message = str(datetime.datetime.now()) + \
              " ;_Title:" + docTitle + \
              " ;_Transactions:" + separator.join(args.GetTransactionNames()) + \
              " ;_Added:" + separator.join(str(ele.IntegerValue) for ele in args.GetAddedElementIds()) + \
              " ;_Deleted:" + separator.join(str(ele.IntegerValue) for ele in args.GetDeletedElementIds()) + \
              " ;_Modified:" + separator.join(str(ele.IntegerValue) for ele in args.GetModifiedElementIds()) + \
              "\n"

    if os.path.exists(cloudLogLocation):
        try:
            cloudLogger.Log(message, user)
        except:
            pass
    else:
        try:
            localLogger.Log(message, user)
        except:
            pass

# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    #try:
    #__rvt__.Application.DocumentChanged += (Logger.test_function)
    #__rvt__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)
    #__rvt__.Application.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    #HOST_APP.app.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    #except:
        #print("Logging Disabled.")
    #message =
    impUtil = CommandUtils.CommandReplacement(__rvt__, "ID_FILE_IMPORT", CommandUtils.ImportReplacement)

    #__rvt__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](viewActivated_handler_function)
    __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    #__rvt__.DialogBoxShowing  += EventHandler[DialogBoxShowingEventArgs](event_handler_function)

    return True

if __name__ == '__main__':
    print('Please do not click this button again.')