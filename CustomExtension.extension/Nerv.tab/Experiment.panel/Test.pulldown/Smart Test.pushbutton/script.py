import os
import os.path as op
import pickle as pl
import clr
import datetime
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
from os import path

__doc__ = 'Keep views synchronized. This means that as you pan and zoom and '\
          'switch between Plan and RCP views, this tool will keep the views '\
          'in the same zoomed area so you can keep working in the same '\
          'area without the need to zoom and pan again.\n'\
          'This tool works best when the views are maximized.'

class Logger:
    # File location for logging
    fileLocation = ""
    # Constructor
    def __init__(self, address):
        self.fileLocation = address
    #Logger
    def Log(self, content, user):
        date = datetime.datetime
        if not path.exists(self.fileLocation):
            logFile = open(self.fileLocation, "w")
            logFile.write(str(datetime.datetime) + "_" + user + "_" + "Log Start")
            logFile.close()

        try:
            writeFile = open(self.fileLocation, "a+")
            writeFile.write(content)
            writeFile.close()
        except:
            print("Failed")

def log_function(sender, args):
    event_uidoc = sender.ActiveUIDocument
    event_doc = sender.ActiveUIDocument.Document
    logger = Logger("\\\\stvgroup.stvinc.com\\p\\NYNY\\Practices\\Hazem Kahla\\RevitLogs\\"
                    + str(datetime.date.today()) + "_" +
                    str(sender.ActiveUIDocument.Document.Application.Username) + ".txt" )
    separator = ","
    docTitle = args.GetDocument().Title
    message = str(datetime.datetime) + \
              " ;_Title:" + docTitle + \
              " ;_Transactions:" + separator.join(args.GetTransactionNames()) + \
              " ;_Added:" + separator.join(args.GetAddedElementIds()) + \
              " ;_Deleted:" + separator.join(args.GetDeletedElementIds()) + \
              " ;_Modified:" + separator.join(args.GetModifiedElementIds())
    logger.Log(message, sender.ActiveUIDocument.Document.Application.Username)

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


SYNC_VIEW_ENV_VAR = 'SYNCVIEWACTIVE'
# todo: sync views - 3D


def copyzoomstate1(sender, args):
    if script.get_envvar(SYNC_VIEW_ENV_VAR):
        event_uidoc = sender.ActiveUIDocument
        event_doc = sender.ActiveUIDocument.Document
        active_ui_views = event_uidoc.GetOpenUIViews()
        current_ui_view = None
        for active_ui_view in active_ui_views:
            if active_ui_view.ViewId == args.CurrentActiveView.Id:
                current_ui_view = active_ui_view

        if isinstance(args.CurrentActiveView, DB.ViewPlan):
            project_name = op.splitext(op.basename(event_doc.PathName))[0]
            data_filename = project_name + '_pySyncRevitActiveViewZoomState'
            data_file = script.get_instance_data_file(data_filename)

            cornerlist = current_ui_view.GetZoomCorners()

            vc1 = cornerlist[0]
            vc2 = cornerlist[1]
            p1 = Point()
            p2 = Point()
            p1.x = vc1.X
            p1.y = vc1.Y
            p2.x = vc2.X
            p2.y = vc2.Y

            f = open(data_file, 'w')
            pl.dump(p1, f)
            pl.dump(p2, f)
            f.close()

        logFile = open("\\\\stvgroup.stvinc.com\\p\\NYNY\\Practices\\Hazem Kahla\\RevitLogs\\"
                + str(datetime.date.today()) + "_" +
                str(sender.ActiveUIDocument.Document.Application.Username) + ".txt", "w")
        logFile.write(str(datetime.datetime) + "_" + "LouM" + "_" + "Log Start")
        logFile.close()


def applyzoomstate1(sender, args):
    if script.get_envvar(SYNC_VIEW_ENV_VAR):
        event_uidoc = sender.ActiveUIDocument
        event_doc = sender.ActiveUIDocument.Document
        active_ui_views = event_uidoc.GetOpenUIViews()
        current_ui_view = None
        for active_ui_view in active_ui_views:
            if active_ui_view.ViewId == args.CurrentActiveView.Id:
                current_ui_view = active_ui_view

        if isinstance(args.CurrentActiveView, DB.ViewPlan):
            project_name = op.splitext(op.basename(event_doc.PathName))[0]
            data_filename = project_name + '_pySyncRevitActiveViewZoomState'
            data_file = script.get_instance_data_file(data_filename)
            f = open(data_file, 'r')
            p2 = pl.load(f)
            p1 = pl.load(f)
            f.close()
            vc1 = DB.XYZ(p1.x, p1.y, 0)
            vc2 = DB.XYZ(p2.x, p2.y, 0)
            current_ui_view.ZoomAndCenterRectangle(vc1, vc2)
        logFile = open("\\\\stvgroup.stvinc.com\\p\\NYNY\\Practices\\Hazem Kahla\\RevitLogs\\"
                       + str(datetime.date.today()) + "_" +
                       str(sender.ActiveUIDocument.Document.Application.Username) + ".txt", "w")
        logFile.write(str(datetime.datetime) + "_" + "LouM" + "_" + "Log Start")
        logFile.close()

def togglestate1():
    new_state = not script.get_envvar(SYNC_VIEW_ENV_VAR)
    script.set_envvar(SYNC_VIEW_ENV_VAR, new_state)
    script.toggle_icon(new_state)


# noinspection PyUnusedLocal
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    try:
        __rvt__.ViewActivating += \
            framework.EventHandler[
                UI.Events.ViewActivatingEventArgs](copyzoomstate1)
        __rvt__.ViewActivated += \
            framework.EventHandler[
                UI.Events.ViewActivatedEventArgs](applyzoomstate1)
        return True
    except Exception:
            return False


if __name__ == '__main__':
    togglestate1()