
import sys, clr, os, re
import ConfigParser
from os.path import expanduser
# Set system path

from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation, IFamilyLoadOptions,\
    FamilySymbol, DWGImportOptions, ImportColorMode, SaveAsOptions, Options, PolyLine, Line, GeometryInstance, Solid
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
import datetime, os


__doc__ = 'To be run in a Revit Model.'\
          'Step 1: Please select the folder that contains Revit families.'\
          'Step 2: Please select the destination folder to save new families.'\
          'Note: Please check the log after running this. ' \
          'Program will not modify or upgrade families despite it saying so in revit.'

def GetLinesFromPolylines(polyline):
    polypoints1 = []
    polypoints2 = []
    lines = []
    coords = polyline.GetCoordinates()
    for coord in coords:
        polypoints1.append(coord)
        polypoints2.append(coord)

    polypoints1 = polypoints1[:-1]
    polypoints2 = polypoints2[1:]
    n = 0
    for a in polypoints1:
        try:
            line = Line.CreateBound(a, polypoints2[n])
            lines.append(line)
        except Exception as e:
            print(str(e))
        n = n + 1
    return lines

def GetLinesFromGeo(GeometryInstance):
    position = GeometryInstance.Transform
    lines = []
    for line in GeometryInstance.GetSymbolGeometry():
        try:
            lines.append(line.CreateTransformed(position))
        except Exception as e:
            print(e)
    return lines

def IteratorList(iterator):
    list = []
    for i in iterator:
        list.append(i)
    return list
def ProcessGeometry(list):
    bool = True
    curves = list
    n = 0
    while bool and n < 20:
        geometryInstance = filter(lambda x: type(x) == GeometryInstance, curves)
        polylines = filter(lambda x: type(x) == PolyLine, curves)
        nonploy = filter(lambda x: type(x) != PolyLine and type(x) != GeometryInstance and type(x) != Solid, curves)
        if IteratorList(geometryInstance) or IteratorList(polylines):
            curves = []
            for i in nonploy:
                curves.append(i)
            # print(len(curves))
            for poly in polylines:
                explodeLines = GetLinesFromPolylines(poly)
                curves.extend(explodeLines)
            for geo in geometryInstance:
                lines = GetLinesFromGeo(geo)
                curves.extend(lines)
        else:
            bool = False
        n += 1

    return curves
def flatten(g):
	for i in g:
		try:
			br1 = (str(i).index('[(')+2)
			br2 = (str(i).index(')]')-2)
			yield str(i)[br1:br2]
		except:
			flatten(i)

def getgeometry(x):
	for i in x:
		try:
			yield getgeometry(i.GetInstanceGeometry())
		except:
			try:
				yield i.Center
			except:
				try:
					yield i.Origin
				except:
					try:
						yield i.GetCoordinates()
					except:
						pass

def StringinStrings(strings, source):
    result = False
    for s in strings:
        if s in source:
            result = True
            break
    return result


def DivideCleanString(divider1, divider2, string, keywordstoRemove):
    stringList = string.upper().split(divider1)
    returnString = ""
    for s in stringList:
        reconstructString = ""
        subList = s.split(divider2)
        for k in keywordstoRemove:
            try:
                subList.remove(k)
            except:
                pass
        if subList:
            for sub in subList:
                if not RepresentsInt(sub):
                    reconstructString += sub
                    reconstructString += divider2
            reconstructString = reconstructString[0: len(reconstructString) - 1]
        if reconstructString != "":
            returnString += reconstructString
            returnString += divider1
    returnString = returnString[0 : len(returnString) - 1]

    return returnString


def CleanListandReconstruct(keywords, stringList):
    words = []
    for s in stringList:
        try:
            words.append(s.upper())
        except:
            pass
    for k in keywords:
        try:
            words.remove(k.upper())
        except:
            pass
    return words

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def UniqueName(proposedName, namesList):
    num = 1
    nameIteration = proposedName + ' ' + str(num)
    while num < 999:
        if not proposedName in namesList:
            return proposedName
            break
        elif not nameIteration in namesList:
            return nameIteration
            break
        else:
            num += 1
            nameIteration = proposedName + ' ' + str(num)
            continue

def CleanUpString(string, keywords, splitters):
    returnString = ""
    for splitter in splitters:
        words = string.split(splitter)
        for word in words:
            if word == "KPF" or RepresentsInt(word):
                words.remove(word)
        for w in words:
            w.split()

class FamilyOption(IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True

	def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		return True


from os.path import isfile, join

processes = ["Create Geometry Families", "Create Annotation Families"]
selProcess = forms.CommandSwitchWindow.show(processes, message='Select Copy Option')


famTemplatePath = app.FamilyTemplatePath
folderPath = forms.pick_folder()
destinationFolderPath = forms.pick_folder()
templateFullName = forms.pick_file(file_ext='rft',
                                   multi_file=False,
                                   unc_paths=False,
                                   init_dir=famTemplatePath,
                                   restore_dir=True,)

onlyfiles = {}
for root, directories, files in os.walk(folderPath, topdown=False):
	for name in files:
		if isfile(join(root, name)) and name[-3: ] == "dwg":
			onlyfiles[name[0: -4]] = (str(os.path.join(root, name)))
	for name in directories:

		if isfile(join(root, name)) and name[-3: ] == "dwg":
			onlyfiles[name[0: -4]] = (str(os.path.join(root, name)))



# Pick Template

# import cad options
importOptions = DWGImportOptions()
importOptions.AutoCorrectAlmostVHLines = True
importOptions.ColorMode = ImportColorMode.BlackAndWhite
importOptions.ThisViewOnly = True

# save as options
saveOp = SaveAsOptions()
saveOp.OverwriteExistingFile = True


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

for cadImport in onlyfiles.keys():
    hostFamDoc = app.NewFamilyDocument(templateFullName)
    view = FilteredElementCollector(hostFamDoc).OfClass(View).FirstElement()
    t = Transaction(hostFamDoc, 'Create new Family')
    t.Start()
    source = onlyfiles[cadImport]
    fileNameToSave = cadImport
    familyManager = hostFamDoc.FamilyManager
    familyManager.NewType(cadImport)
    famId = hostFamDoc.Import(source, importOptions, view)
    t.Commit()
    ele = hostFamDoc.GetElement(famId[1])
    try:
        geometries = ele.get_Geometry(Options())
        # lines = ele.GetGeometryObjectFromReference(Reference(ele))
        list = geometries.GetEnumerator()
    except:
        list = []
    for obj in list:
        allGeom = []
        geo = obj.SymbolGeometry
    if selProcess == "Create Geometry Families":
        try:
            famDoc = app.NewFamilyDocument(templateFullName)
            view = FilteredElementCollector(famDoc).OfClass(View).FirstElement()
            t = Transaction(famDoc, 'Create new Family')
            t.Start()
            source = onlyfiles[cadImport]
            fileNameToSave = cadImport
            familyManager = famDoc.FamilyManager
            familyManager.NewType(cadImport)
            famId = famDoc.Import(source, importOptions, view)
            ele = famDoc.GetElement(famId[1])
            lines = ele.get_Geometry(Options())
            #lines = ele.GetGeometryObjectFromReference(Reference(ele))
            list = lines.GetEnumerator()
            for obj in list:
                allGeom = []
                geo = obj.SymbolGeometry
                for m in geo:
                    allGeom.append(m)
                curves = ProcessGeometry(allGeom)
                #print(len(curves))
                for m in curves:
                    try:
                        famDoc.FamilyCreate.NewSymbolicCurve(m, view.SketchPlane)
                    except Exception as e:
                        print(cadImport + " "+ str(e))
            famDoc.Delete(famId[1])
            t.Commit()
            famDoc.SaveAs(destinationFolderPath + "\\" + fileNameToSave + ".rfa", saveOp)
            famDoc.Close()
        except Exception as e:
            print("Fatal Error: " + cadImport + " " + str(e))

    elif selProcess == "Create Annotation Families":
        try:
            famDoc = app.NewFamilyDocument(templateFullName)
            view = FilteredElementCollector(famDoc).OfClass(View).FirstElement()
            t = Transaction(famDoc, 'Create new Family')
            t.Start()
            source = onlyfiles[cadImport]
            fileNameToSave = cadImport
            familyManager = famDoc.FamilyManager
            familyManager.NewType(cadImport)
            famId = famDoc.Import(source, importOptions, view)
            ele = famDoc.GetElement(famId[1])
            lines = ele.get_Geometry(Options())
            # lines = ele.GetGeometryObjectFromReference(Reference(ele))
            list = lines.GetEnumerator()
            for obj in list:
                allGeom = []
                geo = obj.SymbolGeometry
                for m in geo:
                    allGeom.append(m)
                curves = ProcessGeometry(allGeom)
                # print(len(curves))
                for m in curves:
                    try:
                        famDoc.FamilyCreate.NewDetailCurve(view, m)
                    except Exception as e:
                        print(cadImport + " " + str(e))
            famDoc.Delete(famId[1])
            t.Commit()
            famDoc.SaveAs(destinationFolderPath + "\\" + fileNameToSave + ".rfa", saveOp)
            famDoc.Close()
        except Exception as e:
            print("Fatal Error: " + cadImport + " " + str(e))



