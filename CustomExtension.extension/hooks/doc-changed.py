from Autodesk.Revit.UI import RevitCommandId, Events, TaskDialog
from pyrevit import forms
from pyrevit import EXEC_PARAMS
import Logger
import datetime
import os.path

from os.path import expanduser
home = expanduser("~")

user = __revit__.Username
cloudLogLocation = "C:\\Users\\mengf\\Desktop\\Log\\"
d = datetime.datetime.now()
localPath = home + "\\" + str(d.year) + "_" +\
            str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLlog.txt"


serverPath = cloudLogLocation + user + "\\" + str(d.year) + "_" +\
            str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLog.txt"


localLogger = Logger.MintLogger(localPath)
cloudLogger = Logger.MintLogger(serverPath)

separator = ","
docTitle = EXEC_PARAMS.event_args.GetDocument().Title
message = str(datetime.datetime.now()) + \
          " ;_Title:" + docTitle + \
          " ;_Transactions:" + separator.join(EXEC_PARAMS.event_args.GetTransactionNames()) + \
          " ;_Added:" + separator.join(str(ele.IntegerValue) for ele in EXEC_PARAMS.event_args.GetAddedElementIds()) + \
          " ;_Deleted:" + separator.join(str(ele.IntegerValue) for ele in EXEC_PARAMS.event_args.GetDeletedElementIds()) + \
          " ;_Modified:" + separator.join(str(ele.IntegerValue) for ele in EXEC_PARAMS.event_args.GetModifiedElementIds()) +\
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
