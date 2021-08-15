
import sys, clr, re, bs4
import ConfigParser
from os.path import expanduser


# body
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, ViewSchedule, View, ImportInstance, XYZ
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
import time
uiapp = UIApplication(doc.Application)
application = uiapp.Application
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script, coreutils
from pyrevit import forms

# logging module
import logging
import datetime
userName = application.Username
logFile = '\\\\Uspadgv1dcl01\\NY BIM GROUP\\Tools\\Repo\\pyRevit_custom_Mint\\logs\\' + str(datetime.date.today()) + "_" + userName + '_applog.log'
logging.basicConfig(filename=logFile, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

__doc__ = 'Print all viewports element id and view names'

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)


from System import EventHandler, Uri
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
from Autodesk.Revit.DB import TextNoteType, Viewport
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, IdlingEventArgs
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import SendKeys

def ViewsCheck(doc):
    modelLst = []
    viewports = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
    for i in viewports:
        parameters = ""
        name = i.LookupParameter('View Name').AsString()
        id = i.Id.ToString()
        parameters = id + ", " + name
        modelLst.append(parameters)
    return modelLst


out = ViewsCheck(doc)
for o in out:
    print(o)