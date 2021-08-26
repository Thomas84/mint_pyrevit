import os.path
import datetime
import Logger
import ConfigUtils
from Autodesk.Revit.UI import TaskDialog

def document_opened_sync_function(sender, args):
    TaskDialog.Show("1", "1")
    time = datetime.datetime.now()
    documentTitle = args.GetDocument().Title
    documentCode = str(args.GetDocument().GetHashCode())
    ConfigUtils.WriteModelOpenTimeConfig(documentTitle, documentCode, time)


def document_synced_sync_function(sender, args):
    time = datetime.datetime.now()
    documentTitle = args.GetDocument().Title
    documentCode = str(args.GetDocument().GetHashCode())
    ConfigUtils.WriteModelOpenTimeConfig(documentTitle, documentCode, time)


def document_closed_sync_function(sender, args):
    documentTitle = args.GetDocument().Title
    documentCode = str(args.GetDocument().GetHashCode())
    ConfigUtils.WipeTimeConfig(documentTitle, documentCode)


def document_changed_sync_function(sender, args):
    time = datetime.datetime.now()
    documentTitle = args.GetDocument().Title
    documentCode = str(args.GetDocument().GetHashCode())
    lock = ConfigUtils.CheckSyncTimeConfig(documentTitle, documentCode, time, [4, 3, 2, 1])
    if lock:
        pass
