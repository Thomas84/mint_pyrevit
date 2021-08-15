
import sys, clr
import ConfigParser
from os.path import expanduser

import Selection
clr.AddReference('System')
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation

from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, 'Tag Selected Element')
t.Start()
selection = Selection.get_selected_elements(doc)
for a in selection:
    location = a.Location
    IndependentTag.Create(doc, doc.ActiveView.Id, Reference(a), True, TagMode.TM_ADDBY_MULTICATEGORY, TagOrientation.Horizontal, location.Point)
    print(location.Point)
t.Commit()
