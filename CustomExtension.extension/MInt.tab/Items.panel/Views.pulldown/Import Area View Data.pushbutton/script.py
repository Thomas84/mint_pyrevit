import sys, clr
import ConfigParser
from os.path import expanduser


from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory, \
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray
from Autodesk.Revit.DB import Level, View, BuiltInParameter, ViewPlan, \
    Area, AreaTag, BoundarySegment, CopyPasteOptions, ElementTransformUtils, SpatialElement, \
    SpatialElementBoundaryOptions, ElementId, SpatialElementTag

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import forms
from System.Collections.Generic import List

__doc__ = 'Import areas from source model, ' \
          'Must have identicaly named source view ' \
          'and destination view. Needs to be run in the source document' \
          '1. Select the Area View to copy to from the list' \
          '2. Select the source document'


# Get Area Plans

def GetAreaPlans(sdoc):
    plans = FilteredElementCollector(sdoc).OfClass(ViewPlan).ToElements()
    areaPlans = {}
    for plan in plans:
        if plan != None:
            if plan.AreaScheme != None:
                # print(plan.Name)
                if plan.Name != None:
                    areaPlans[plan.Name] = plan
    return areaPlans


def GetAreaData(sdoc, view):
    result = []
    areas = FilteredElementCollector(sdoc, view.Id).OfClass(SpatialElement).ToElements()
    filteredAreas = []
    for area in areas:
        # print(area.Category.Name)
        if area.Category.Name == "Areas":
            filteredAreas.append(area.Id)
    # areaIds = FilteredElementCollector(sdoc, view.Id).OfClass(SpatialElement).ToElementIds()
    areaTags = FilteredElementCollector(sdoc, view.Id).OfClass(SpatialElementTag).ToElementIds()
    arealines = FilteredElementCollector(sdoc, view.Id).OfCategory(BuiltInCategory.OST_AreaSchemeLines).ToElementIds()
    result.extend(arealines)
    '''
    op = SpatialElementBoundaryOptions()

    for area in areas:
        bounds = area.GetBoundarySegments(op)
        for bound in bounds:
            for b in bound:
                if not b.ElementId in result and b.ElementId.IntegerValue > 0:
                    result.append(b.ElementId)
    '''
    result.extend(filteredAreas)
    result.extend(areaTags)
    return result


areaPlans = GetAreaPlans(doc)
selViews = forms.SelectFromList.show(areaPlans.keys(), multiselect=True, button_name='Select Area Plans')

# Get Source Document

activeDocuments = doc.Application.Documents

activeDocs = {}
for document in activeDocuments:
    activeDocs[document.Title] = document

selDoc = forms.SelectFromList.show(activeDocs.keys(), multiselect=False, button_name='Select Source Document')

sourceDoc = activeDocs[selDoc]
sourceAreaPlans = GetAreaPlans(sourceDoc)

t = Transaction(doc, 'Copy Area Data')
t.Start()
for viewName in selViews:
    if viewName in sourceAreaPlans.keys():
        idsToCopy = GetAreaData(sourceDoc, sourceAreaPlans[viewName])
        # print(idsToCopy)
        trans = None
        op = CopyPasteOptions()
        element_collection = List[ElementId](idsToCopy)
        ElementTransformUtils.CopyElements(sourceAreaPlans[viewName], element_collection, areaPlans[viewName], trans,
                                           op)
    else:
        print("cannot find {0} in source doc".format(viewName))

t.Commit()
