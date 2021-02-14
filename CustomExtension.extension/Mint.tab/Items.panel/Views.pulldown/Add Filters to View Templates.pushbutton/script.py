
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
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation, IFamilyLoadOptions,\
    FamilySymbol, FilterElement
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from pyrevit import revit, DB, forms
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

processes = ["Copy from existing view templates", "Add filters"]
selProcess = forms.SelectFromList.show(processes, multiselect=False,  button_name='Select processes')

if selProcess == "Add filters":
    ff = {}
    filters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()

    for filter in filters:
        ff[filter.Name] = filter
    selFilters = forms.SelectFromList.show(ff.keys(), multiselect=True,  button_name='Select Filters')

    vv= {}
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if view.IsTemplate:
            vv[view.Title] = view
    selViews = forms. SelectFromList.show(vv.keys(), multiselect=True, button_name='Select Templates')

    t = Transaction(doc, 'Add Filter to Templates')
    t.Start()
    for selectedView in selViews:
        view = vv[selectedView]
        for selectedFilter in selFilters:
            filter = ff[selectedFilter].Id
            try:
                view.AddFilter(filter)
            except:
                pass
    t.Commit()

elif selProcess == "Copy from existing view templates":

    vv= {}
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if view.IsTemplate:
            vv[view.Title] = view
    selView = forms. SelectFromList.show(vv.keys(), multiselect=False, button_name='Select Source Template')
    targetViews = forms. SelectFromList.show(vv.keys(), multiselect=True, button_name='Select Target Template')


    filterData = []
    source = vv[selView]
    filters = source.GetFilters()
    for filter in filters:
        overrides = source.GetFilterOverrides(filter)
        vis = source.GetFilterVisibility(filter)
        filterData.append([filter, overrides, vis])
    t = Transaction(doc, 'Add Filter to Templates')
    t.Start()
    for targetView in targetViews:
        target = vv[targetView]
        for fd in filterData:
            try:
                target.AddFilter(fd[0])
                target.SetFilterOverrides(fd[0], fd[1])
                target.SetFilterVisibility(fd[0], fd[2])
            except:
                pass

    t.Commit()
