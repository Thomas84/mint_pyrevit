import sys, clr
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\MintTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\MintTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)

clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, Family, Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, RevitLinkInstance, \
    RevitLinkType, View, BoundingBoxXYZ, BuiltInParameter, ViewSet, ViewSheetSet, PrintRange, ViewSheet
from Autodesk.Revit.UI import TaskDialog

def event_handler_function(sender, args):
    TaskDialog.Show("Test", "View Activated")
    # do the even stuff here
    # I'm using ViewActivating event here as example.
    # The handler function will be executed every time a Revit view is activated:

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    __rvt__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)