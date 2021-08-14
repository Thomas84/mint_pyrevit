
import sys
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

def Importcsv(Filename):
    flat_list = []
    with open(Filename, 'r') as f:
        reader = csv.reader(f)
        Lst = list(reader)
        for sublist in Lst:
            for item in sublist:
                flat_list.append(item)
    return (flat_list)


import System, Selection
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol, Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementCategoryFilter, ReferenceIntersector, \
    FindReferenceTarget, SpatialElementBoundaryOptions
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.UI import TaskDialog
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

__doc__ = 'Selects room bounding elements of selected room'
currentChoice = []
def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

for i in get_selected_elements(doc):
    currentChoice.append(i)

class RoomsSelectionFilter(ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
		if element.Category.Name == "Rooms":
			return True
		else:
			return False

roomFilter = RoomsSelectionFilter()
selection = []
choices = uidoc.Selection

if not currentChoice:
    ref = choices.PickObject(ObjectType.Element, roomFilter, "Pick One Element")
    selection.append(doc.GetElement(ref.ElementId))
elif currentChoice[0].Category.Name != "Rooms":
    TaskDialog.Show("Error", "Selected Element is not a room")
else:
    # TO DO: ADD A LIST TO ALLOW USERS TO CHOOSE WHICH WORKSET THEY WANT
    selection.append(currentChoice[0])

elements = []
# convenience variable for first element in selection
for i in selection:
    loops = i.GetBoundarySegments(SpatialElementBoundaryOptions())
    for l in loops:
        for s in l:
            element = s.ElementId
            #print(element)
            elements.append(doc.GetElement(element))
revit.get_selection().set_to(elements)



