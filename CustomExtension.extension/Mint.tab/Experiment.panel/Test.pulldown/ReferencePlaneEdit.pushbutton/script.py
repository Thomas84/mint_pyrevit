
import sys, clr, os, re
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
# print(os.path.dirname(os.path.realpath(__file__).split(".extension")[0] + ".extension\\packages\\"))
cfgfile = open(home + "\\MintTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\MintTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)
import Selection
clr.AddReference('System')
from rpw import revit, db, ui
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation, IFamilyLoadOptions,\
    FamilySymbol, DatumExtentType, Level, Line
from Autodesk.Revit.UI.Selection import ObjectType
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
import datetime, os
from pyrevit import HOST_APP, framework
import Autodesk.Revit.DB.ExtensibleStorage
import uuid
import shutil

__doc__ = 'To be run in a Revit Model.'\
          'Step 1: Please select the folder that contains Revit families.'\
          'Step 2: Please select the destination folder to save new families.'\
          'Note: Please check the log after running this. ' \
          'Program will not modify or upgrade families despite it saying so in revit.'


def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

class ReferencePlaneSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Reference Planes":
			return True
		else:
			return False

refFilter = ReferencePlaneSelectionFilter()
selection = get_selected_elements(doc)
viewType = doc.ActiveView.ViewType

if "Section" in viewType.ToString() or "Elevation" in viewType.ToString():
    if len(selection) != 0:
        pass
    else:
        selection = []
        selections = uidoc.Selection.PickObjects(ObjectType.Element, refFilter, "Pick Pipe")
        for s in selections:
            selection.append(doc.GetElement(s.ElementId))

    levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    levelData = {}
    levelDic = {}
    for i in levels:
        levelData[i.Name] = i.Elevation

    bottom = forms.SelectFromList.show(levelData.keys(), button_name='Select Bottom Level for the Reference Plane',
                                           multiselect=False)
    top = forms.SelectFromList.show(levelData.keys(), button_name='Select Top Level for the Reference Plane',
                                           multiselect=False)
    offsetInput = str(forms.GetValueWindow.show(None,
            value_type='string',
            default=str(0.00),
            prompt='Please Enter offset in feet',
            title='Offset'))
    bottomHeight = levelData[bottom]
    topHeight = levelData[top]

    t = Transaction(doc, 'Change Planes')
    t.Start()

    if selection:
        for sel in selection:
            #print(sel.FreeEnd)
            #print(sel.BubbleEnd)
            endPt1 = sel.GetCurvesInView(DatumExtentType.Model, doc.ActiveView)[0].GetEndPoint(0)
            endPt2 = sel.GetCurvesInView(DatumExtentType.Model, doc.ActiveView)[0].GetEndPoint(1)

            newEndPt1 = XYZ(endPt1.X, endPt1.Y, bottomHeight + float(offsetInput))
            newEndPt2 = XYZ(endPt2.X, endPt2.Y, topHeight - float(offsetInput))
            newLine = Line.CreateBound(newEndPt1, newEndPt2)
            sel.SetCurveInView(DatumExtentType.Model, doc.ActiveView, newLine)

    t.Commit()
else:
    forms.alert("Please go to an elevation or section and select the reference plane")
