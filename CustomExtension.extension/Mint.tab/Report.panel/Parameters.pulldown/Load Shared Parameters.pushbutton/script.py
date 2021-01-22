from pyrevit.framework import List
from pyrevit import revit, DB, forms
import re, clr, os, threading
import xlsxwriter

clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
    OpenOptions, WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, RevitLinkType, ViewFamilyType, \
    ViewFamily, View3D, IndependentTag, BuiltInParameter, FamilyType, BuiltInParameter, BuiltInCategory, \
    BuiltInParameterGroup
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')



# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Report the selected Model Element Quality Check outcome in an Excel file.' \
          'Open projects and resave in a specific location.' \
          'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Pick an action, #view specific will create default 3d view with current visibility
def BindSharedParameter():
    cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Sheets)
    catSet = application.Create.NewCategorySet()
    catSet.Insert(cat)
    spFile = application.OpenSharedParameterFile()
    names = []
    params = {}
    for dG in spFile.Groups:
        if dG.Name == "Title Block":
            for eD in dG.Definitions:
                if "Reference" in eD.Name:
                    names.append(eD.Name)
                    params[eD.Name] = eD
    names.sort()
    print(names)
    for n in names:
        param = params[n]
        newIB = application.Create.NewInstanceBinding(catSet)
        doc.ParameterBindings.Insert(param, newIB, BuiltInParameterGroup.PG_TEXT)

t = Transaction(doc, 'Load Shared Parameters')
t.Start()
BindSharedParameter()
t.Commit()
