
import sys, clr, os
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
print(os.path.dirname(os.path.realpath(__file__).split(".extension")[0] + ".extension\\packages\\"))
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
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation, IFamilyLoadOptions
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

class FamilyOption(IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True

	def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		return True

#print(expanduser("~"))

from os import listdir
from os.path import isfile, join

folderPath = forms.pick_folder()
# onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
onlyfiles = []
for root, directories, files in os.walk(folderPath, topdown=False):
	for name in files:
		if isfile(join(root, name)):
			onlyfiles.append(str(os.path.join(root, name)))
	for name in directories:

		if isfile(join(root, name)):
			onlyfiles.append(str(os.path.join(root, name)))


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, 'Test')
t.Start()

for i in onlyfiles:
    doc.LoadFamily(i, FamilyOption())

t.Commit()