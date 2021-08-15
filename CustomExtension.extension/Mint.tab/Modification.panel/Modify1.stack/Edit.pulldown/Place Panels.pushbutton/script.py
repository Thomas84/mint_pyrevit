
import sys, clr
import ConfigParser
from os.path import expanduser


import System, Selection
import System.Threading, System.Threading.Tasks
import csv
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory, \
	RevitLinkInstance, UV, XYZ,SpatialElementBoundaryOptions, CurveArray, AdaptiveComponentInstanceUtils, \
	Level, BuiltInParameter, FamilySymbol, ElementTransformUtils, IFamilyLoadOptions
from Autodesk.Revit.UI import TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
from Autodesk.Revit.UI import TaskDialog, UIApplication
from math import *

__doc__ = 'Import rooms to space from link model'

import clr
from os.path import isfile, join
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

def Importcsv(Filename):
    flat_list = []
    with open(Filename, 'r') as f:
        reader = csv.reader(f)
        Lst = list(reader)
        for sublist in Lst:
            flat_list.append(sublist)
            #for item in sublist:
                #flat_list.append(item)
    return flat_list

class FamilyOption(IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True

	def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		return True

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, 'Place an Adaptive Component.')
t.Start()


collectorCSVFile = forms.pick_file(file_ext='csv', multi_file=True, unc_paths=False)
pointDataLength = 0
pointData = {}
for c in collectorCSVFile:
	file = Importcsv(c)
	pointDataLength += len(file)
	fileName = os.path.basename(c).replace(".csv", "")
	pointData[fileName] = file


# create a filtered element collector set to Category OST_Mass and Class FamilySymbol

famtypeitr = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).OfClass(FamilySymbol).ToElementIds()
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
levelHeightData = {}
heights = []
for level in levels:
	height = level.Elevation
	name = level.Name
	heights.append(height)
heights.sort(key = float)
heights.append(999999999)
for l in levels:
	index = heights.index(l.Elevation)
	levelHeightData[l.Name] = [l.Elevation, heights[index + 1]]
#famtypeitr.Reset()
count = 0
# Search Family Symbols in document.
with forms.ProgressBar(title='Generating Panels') as pb:
	# do stuff

	for symbName in pointData.keys():
		famsymb = ""
		#print(symbName)
		pData = pointData[symbName]
		#print(pData)
		for item in famtypeitr:
			famtypeID = item
			famsymbName = doc.GetElement(famtypeID)
			# If the FamilySymbol is the name we are looking for, create a new instance.
			if famsymbName.Family.Name == symbName:
				famsymb = famsymbName
		#print(famsymb)
		#print(famsymb.Name)
		if famsymb:
			for p in pData:
				adaptComp = AdaptiveComponentInstanceUtils.CreateAdaptiveComponentInstance(doc, famsymb)
				adptPoints = AdaptiveComponentInstanceUtils.GetInstancePlacementPointElementRefIds(adaptComp)

				# Starting adaptive point locations.  get_Element returns a Reference Point
				aPt1 = doc.GetElement(adptPoints[0])
				aPt2 = doc.GetElement(adptPoints[1])
				aPt3 = doc.GetElement(adptPoints[2])
				aPt4 = doc.GetElement(adptPoints[3])

				# Desired Adaptive Point Locations
				p1 = p[0].replace("\"", "").replace("{", "").replace("}", "").split(",")
				p2 = p[1].replace("\"", "").replace("{", "").replace("}", "").split(",")
				p3 = p[2].replace("\"", "").replace("{", "").replace("}", "").split(",")
				p4 = p[3].replace("\"", "").replace("{", "").replace("}", "").split(",")

				loc1 = XYZ(float(p1[0]), float(p1[1]), float(p1[2]))
				loc2 = XYZ(float(p2[0]), float(p2[1]), float(p2[2]))
				loc3 = XYZ(float(p3[0]), float(p3[1]), float(p3[2]))
				loc4 = XYZ(float(p4[0]), float(p4[1]), float(p4[2]))

				midHeight = ((loc1 + loc2 + loc3 + loc4)/4).Z
				for levelData in levelHeightData.keys():
					heights = levelHeightData[levelData]
					if midHeight > heights[0] and midHeight < heights[1]:
						adaptComp.LookupParameter("Panel Level").Set(levelData)
				# Some vector math to get the translation for MoveElement()
				trans1 = loc1.Subtract(aPt1.Position)
				trans2 = loc2.Subtract(aPt2.Position)
				trans3 = loc3.Subtract(aPt3.Position)
				trans4 = loc4.Subtract(aPt4.Position)

				# Position Adaptive Component using MoveElement()
				ElementTransformUtils.MoveElement(doc, adptPoints[0], trans1)
				ElementTransformUtils.MoveElement(doc, adptPoints[1], trans2)
				ElementTransformUtils.MoveElement(doc, adptPoints[2], trans3)
				ElementTransformUtils.MoveElement(doc, adptPoints[3], trans4)
				pb.update_progress(count, pointDataLength)
				count += 1
t.Commit()


