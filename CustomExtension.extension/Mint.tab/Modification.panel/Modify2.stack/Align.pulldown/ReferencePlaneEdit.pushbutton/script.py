
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
    FamilySymbol, DatumExtentType, Level, Line, ViewSection, ViewFamily, BoundingBoxXYZ, Transform
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
vft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
sectionType = None
for v in vft:
    if ViewFamily.Section.ToString() == v.ViewFamily.ToString():
        sectionType = v
        break

if sectionType != None:

#if "Section" in viewType.ToString() or "Elevation" in viewType.ToString():
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
        levelData[i.Name] = i.ProjectElevation

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
            sections = []
            try:
                bb1 = BoundingBoxXYZ()
                t1 = Transform.Identity
                t1.Origin = XYZ(0, 0, 0)
                t1.BasisX = sel.GetPlane().Normal
                t1.BasisY = sel.GetPlane().XVec
                t1.BasisZ = sel.GetPlane().YVec
                bb1.Transform = t1
                view1 = ViewSection.CreateSection(doc, sectionType.Id, bb1)
                view1.CropBoxActive = False
                sections.append(view1)
            except:
                pass
            try:
                bb2 = BoundingBoxXYZ()
                t2 = Transform.Identity
                t2.Origin = XYZ(0, 0, 0)
                t2.BasisX = sel.GetPlane().Normal
                t2.BasisY = sel.GetPlane().XVec
                t2.BasisZ = sel.GetPlane().YVec
                bb2.Transform = t2
                view2 = ViewSection.CreateSection(doc, sectionType.Id, bb2)
                view2.CropBoxActive = False
                sections.append(view2)
            except:
                pass
            try:
                bb22 = BoundingBoxXYZ()
                t22 = Transform.Identity
                t22.Origin = XYZ(0, 0, 0)
                t22.BasisX = sel.GetPlane().XVec
                t22.BasisY = sel.GetPlane().Normal
                t22.BasisZ = sel.GetPlane().YVec
                bb22.Transform = t22
                view22 = ViewSection.CreateSection(doc, sectionType.Id, bb22)
                view22.CropBoxActive = False
                sections.append(view22)
            except:
                pass
            try:
                bb3 = BoundingBoxXYZ()
                t3 = Transform.Identity
                t3.Origin = XYZ(0, 0, 0)
                t3.BasisX = sel.GetPlane().YVec
                t3.BasisY = sel.GetPlane().Normal
                t3.BasisZ = sel.GetPlane().XVec
                bb3.Transform = t3
                view3 = ViewSection.CreateSection(doc, sectionType.Id, bb3)
                view3.CropBoxActive = False
                sections.append(view3)
            except:
                pass
            try:
                bb4 = BoundingBoxXYZ()
                t4 = Transform.Identity
                t4.Origin = XYZ(0, 0, 0)
                t4.BasisX = sel.GetPlane().XVec
                t4.BasisY = sel.GetPlane().YVec
                t4.BasisZ = sel.GetPlane().Normal
                bb4.Transform = t4
                view4 = ViewSection.CreateSection(doc, sectionType.Id, bb4)
                view4.CropBoxActive = False
                sections.append(view4)
            except:
                pass
            try:
                bb5 = BoundingBoxXYZ()
                t5 = Transform.Identity
                t5.Origin = XYZ(0, 0, 0)
                t5.BasisX = sel.GetPlane().YVec
                t5.BasisY = sel.GetPlane().XVec
                t5.BasisZ = sel.GetPlane().Normal
                bb5.Transform = t5
                view5 = ViewSection.CreateSection(doc, sectionType.Id, bb5)
                view5.CropBoxActive = False
                sections.append(view5)
            except:
                pass
            #try:
            #print(str(len(sections)))
            for s in sections:
                try:
                    endPt1 = sel.GetCurvesInView(DatumExtentType.Model, s)[0].GetEndPoint(0)
                    #print(endPt1)
                    endPt2 = sel.GetCurvesInView(DatumExtentType.Model, s)[0].GetEndPoint(1)
                    #print(endPt2)
                    newEndPt1 = XYZ(endPt1.X, endPt1.Y, bottomHeight + float(offsetInput))
                    #print(newEndPt1)
                    newEndPt2 = XYZ(endPt2.X, endPt2.Y, topHeight - float(offsetInput))
                    #print(newEndPt2)
                    newLine = Line.CreateBound(newEndPt1, newEndPt2)
                    sel.SetCurveInView(DatumExtentType.Model, s, newLine)
                    #print("Completed")
                except:
                    #print("Edit Failed")
                    pass
                doc.Delete(s.Id)
    t.Commit()
else:
    forms.alert("Please create a section in your model first")
