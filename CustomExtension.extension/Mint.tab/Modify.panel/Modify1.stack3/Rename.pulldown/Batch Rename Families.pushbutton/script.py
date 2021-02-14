
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
clr.AddReference('System')
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation, IFamilyLoadOptions,\
    FamilySymbol
from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import framework
import shutil

__doc__ = 'To be run in a Revit Model. ' \
          'Rename families to SpecNumber-Revit Category-Description.'\
          'Step 1: Please select the folder that contains Revit families.'\
          'Step 2: Please select the destination folder to save new families.'\
          'Note: Please check the log after running this. ' \
          'Program will not modify or upgrade families despite it saying so in revit.'


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
                if not RepresentsInt(sub.strip()):
                    reconstructString += sub.strip()
                    reconstructString += divider2
            reconstructString = reconstructString[0: len(reconstructString) - 1]
        if reconstructString != "":
            returnString += reconstructString.strip()
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


specSections = {"Air Terminals": "23",
"Cable Tray Fittings": "26",
"Cable Tray Runs": "26",
"Cable Trays": "26",
"Casework": "12",
"Columns": "06",
"Communication Devices": "27",
"Conduit Fittings": "26",
"Conduit Runs": "26",
"Conduits": "26",
"Curtain Grids": "08",
"Curtain Panels": "08",
"Curtain Systems": "08",
"Curtain Wall Mullions": "07",
"Data Devices": "27",
"Doors": "08",
"Duct Accessories": "23",
"Duct Fittings": "23",
"Duct Insulations": "23",
"Duct Linings": "23",
"Duct Placeholders": "23",
"Duct Systems": "23",
"Ducts": "23",
"Electrical Circuits": "26",
"Electrical Equipment": "26",
"Electrical Fixtures": "26",
"Electrical Spare/Space Circuits": "26",
"Entourage": "12",
"Fire Alarm Devices": "28",
"Flex Ducts": "23",
"Flex Pipes": "22",
"Floors": "03",
"Furniture": "12",
"Furniture Systems": "12",
"Generic Models": "00",
"HVAC Zones": "23",
"Lighting Devices": "26",
"Lighting Fixtures": "26",
"Mass": "00",
"Mechanical Equipment": "23",
"Mechanical Equipment Set Boundary Lines": "23",
"Mechanical Equipment Sets": "23",
"MEP Fabrication Containment": "23",
"MEP Fabrication Ductwork": "23",
"MEP Fabrication Hangers": "23",
"MEP Fabrication Pipework": "23",
"Nurse Call Devices": "27",
"Pipe Fittings": "22",
"Pipe Insulations": "22",
"Pipe Placeholders": "22",
"Pipe Segments": "22",
"Pipes": "22",
"Piping Systems": "22",
"Planting": "12",
"Plumbing Fixtures": "22",
"Security Devices": "27",
"Site": "12",
"Specialty Equipment": "11",
"Sprinklers": "21",
"Telephone Devices": "27",
"Topography": "31",
"Windows": "08"}

specExceptions = ["Railings", "Structural", "Supports", "Terminations"]

material = {"03": ["CONCRETE"],
            "05": ["METALS", "STEEL", "ALUM", "ALUMINIUM"],
            "06": ["WOOD", "PLASTIC"],
            "04": ["MASONRY", "STONE"]

}

from os.path import isfile, join

folderPath = forms.pick_folder()
destinationFolderPath = forms.pick_folder()
# onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
onlyfiles = {}
for root, directories, files in os.walk(folderPath, topdown=False):
	for name in files:
		if isfile(join(root, name)) and name[-3: ] == "rfa":
			onlyfiles[name[0: -4]] = (str(os.path.join(root, name)))
	for name in directories:

		if isfile(join(root, name)) and name[-3: ] == "rfa":
			onlyfiles[name[0: -4]] = (str(os.path.join(root, name)))

#print(onlyfiles)

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, 'Test')
t.Start()

for i in onlyfiles.values():
    doc.LoadFamily(i, FamilyOption())

t.Commit()


families = {}
familySymbols = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
for s in familySymbols:
    if s.FamilyName in onlyfiles.keys():
        families[s.FamilyName] = s.Family
#print(families)


for familyName in families.keys():
    specNumber = "00"
    family = families[familyName]
    cate = family.FamilyCategory.Name
    familyRegex = re.compile(r'\d\d-\S+.*\s?-\s?\S+.*?')
    if len(familyName.split("-")) >= 3 and \
            familyRegex.findall(familyName) >= 1 and \
            cate.upper() == familyName.split("-")[1]:

        src_fpath = onlyfiles[familyName]
        dest_fpath = onlyfiles[familyName].replace(folderPath, destinationFolderPath)

        try:
            shutil.copy(src_fpath, dest_fpath)
        except IOError as io_err:
            os.makedirs(os.path.dirname(dest_fpath))
            shutil.copy(src_fpath, dest_fpath)
    else:
        if not "Railings" in cate and not"Structural" in cate and not "Supports" in cate and not "Terminations" in cate:
            try:
                specNumber = specSections[cate]
            except:
                pass
        elif "Railings" in cate or "Structural" in cate or "Supports" in cate or "Terminations" in cate:
            for specNum in material.keys():
                for keyword in material[specNum]:
                    if keyword.upper() in familyName.upper():
                        specNumber = specNum
                        break
            if specNumber == "00":
                specNumber = "06"
        else:
            specNumber = "00"

        keywordstoRemove = ["KPF", "_", "-", family.FamilyCategory.Name.ToString().upper()]
        cleanName = specNumber + "-" + \
                    family.FamilyCategory.Name.ToString().upper() + "-" + \
                    DivideCleanString("-", '_', familyName, keywordstoRemove)
        print(familyName + ": " + cleanName)

        src_fpath = onlyfiles[familyName]
        dest_fpath = onlyfiles[familyName].replace(folderPath, destinationFolderPath).replace(familyName, cleanName)

        try:
            shutil.copy(src_fpath, dest_fpath)
        except IOError as io_err:
            os.makedirs(os.path.dirname(dest_fpath))
            shutil.copy(src_fpath, dest_fpath)
