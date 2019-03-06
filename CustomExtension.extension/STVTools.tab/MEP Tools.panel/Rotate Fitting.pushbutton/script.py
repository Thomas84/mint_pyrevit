import clr, math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, FilteredElementCollector, PerformanceAdviser, FamilySymbol,BuiltInCategory, \
    MEPCurveType, RoutingPreferenceRuleGroupType, RoutingConditions, RoutingPreferenceErrorLevel, RoutingPreferenceRule,\
    PreferredJunctionType,Transaction, BuiltInParameter, XYZ, Line, Connector
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import PipeType
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
from collections import defaultdict
from pyrevit import script
from pyrevit import forms


__doc__ = 'Rotate Pipe Fittings connected to pipe'\
          'Click the tool, select the pipe and then the fitting ' \
          'Type in a number you want to rotate and you are good to go,'\
          'Can Take negative Values'
choices = uidoc.Selection
pipeRef = choices.PickObject(ObjectType.Element, "Pick Pipe")
connectorRef = choices.PickObject(ObjectType.Element, "Pick Pipe Fitting")
pipe = doc.GetElement(pipeRef.ElementId)
connector = doc.GetElement(connectorRef.ElementId)
angleInput = str(forms.GetValueWindow.show(None,
        value_type='string',
        default=str(0.00),
        prompt='Please Enter angle',
        title='Angle'))
angle = (float(angleInput)*math.pi)/180
t = Transaction(doc, 'Rotate Fitting')
t.Start()
inn = [connector,pipe]
conns = [0,1]
pointOne = pipe.Location.Curve.GetEndPoint(0)
pointTwo = pipe.Location.Curve.GetEndPoint(1)

def disconnect(curve):
	connectors = curve.ConnectorManager.Connectors
	for conn in connectors:
		if conn.IsConnected:
			for c in conn.AllRefs:
				if conn.IsConnectedTo(c):
					conns[0] = conn
					conns[1] = c
					conn.DisconnectFrom(c)

connectors = inn[0].MEPModel.ConnectorManager.Connectors
for c in connectors:
	if c.GetMEPConnectorInfo().IsPrimary:
		primary = c
		break
	primary = c
loc = inn[0].Location
ductloc = inn[1].Location
# center = primary.CoordinateSystem.BasisZ
# centerrot = XYZ(center.X,center.Y,center.Z)
center = primary.Origin
line = DB.Line.CreateBound(pointOne, pointTwo)
disconnect(inn[1])
ductloc.Rotate(line,angle)
success = loc.Rotate(line,angle)
conns[0].ConnectTo(conns[1])

t.Commit()


