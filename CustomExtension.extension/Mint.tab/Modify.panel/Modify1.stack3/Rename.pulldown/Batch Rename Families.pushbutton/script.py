import clr
import os
import re
import sys
from os.path import expanduser

import ConfigParser

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
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, IFamilyLoadOptions,\
    FamilySymbol
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
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
c = 0
templateName = ""
with forms.ProgressBar(title='Converting Families') as pb:

    famTemplatePath = app.FamilyTemplatePath
    templateFullName = Path.Combine(famTemplatePath, templateName + ".rft")
    famDoc = app.NewFamilyDocument(templateFullName)
    famDoc.SaveAs(fileNameToSave)

t.Commit()

