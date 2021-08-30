import sys, clr
import ConfigParser
from os.path import expanduser
import math
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter, XYZ, Line, Connector
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import PipeType
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB, UI
from pyrevit import forms
import Selection
__doc__ = 'Rotates on Z axis based on object location points or center point of location line'

selection = Selection.get_selected_elements(doc)
rotateobjs = []
if len(selection):
    rotateobjs = selection
else:
    choices = uidoc.Selection
    objRef = choices.PickObjects(ObjectType.Element, "Pick Element you want to rotate")

    for i in objRef:
        connectors = doc.GetElement(i.ElementId)
        rotateobjs.append(connectors)

angleInput = str(forms.GetValueWindow.show(None,
        value_type='string',
        default=str(0.00),
        prompt='Please Enter angle',
        title='Angle'))
angle = (float(angleInput)*math.pi)/180

# Transaction Start
t = Transaction(doc, 'Rotate(Z)')
t.Start()
for connector in rotateobjs:
    loc = connector.Location
    axis = ()
    try:
        pointStart = loc.Curve.GetEndPoint(0)
        pointEnd = loc.Curve.GetEndPoint(1)
        add = pointEnd + pointStart
        mid = add/2.0
        axis = Line.CreateBound(mid, XYZ(mid.X, mid.Y, mid.Z + 1.0))
    except:
        mid = loc.Point
        axis = Line.CreateBound(mid, XYZ(mid.X, mid.Y, mid.Z + 1.0))
    loc.Rotate(axis, angle)

t.Commit()