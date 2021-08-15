import clr
import os
import re
import sys
from os.path import expanduser

import ConfigParser


from Autodesk.Revit.DB import FilteredElementCollector, Transaction, IFamilyLoadOptions, \
    FamilySymbol, BuiltInParameter
from pyrevit import forms

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import shutil

__doc__ = 'To be run in a Revit Model. ' \
          'Rename families to SpecNumber-Revit Category-Description.' \
          'Step 1: Please select the folder that contains Revit families.' \
          'Step 2: Please select the destination folder to save new families.' \
          'Note: Please check the log after running this. ' \
          'Program will not modify or upgrade families despite it saying so in revit.'


def StringinStrings(strings, source):
    result = False
    for s in strings:
        if s in source:
            result = True
            break
    return result


def ConvertToTitleString(string):
    title = ""
    title = string.title().replace("_", " ")
    return title


def RemoveLastUnderdash(s):
    list = s.split("_")
    c = 1
    result = ""
    while c < len(list):
        result += list[c-1]
        c += 1
    result = result + list[len(list)-1]
    return result

def DivideCleanString(divider1, divider2, string, keywordstoRemove):
    #string = RemoveLastUnderdash(string)
    print(string)
    stringList = string.split(divider1)

    subStrings = ""
    returnString = []
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
                #if len(sub.title().strip()) > 2:
                reconstructString += ConvertToTitleString(sub.title().strip())
                    #if not RepresentsInt(sub.title().strip()) and len(sub.title().strip()) > 2:
                    #ConvertToTitleString(sub.title().strip())
                    
            if reconstructString:
                returnString.append(reconstructString.title().strip())
        if len(returnString) > 2:
            des = ""
            for rString in returnString[1:]:
                des += rString
            subStrings = (returnString[0] + "-" + des).title().strip()
        elif len(returnString) == 2:
            subStrings = (returnString[0] + "-" + returnString[1]).title().strip()
        elif len(returnString) == 1:
            subStringsList = returnString[0].split(" ")
            if len(subStringsList) > 1:
                names = subStringsList[:len(subStringsList) // 2]
                descriptions = subStringsList[len(subStringsList) // 2:]
                for name in names:
                    subStrings += name.title().strip()
                subStrings += "-"
                for d in descriptions:
                    subStrings += d.title().strip()
            else:
                subStrings = subStringsList[0]
        else:
            subStrings = ""

    return subStrings


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
            #if word == "KPF" or RepresentsInt(word):
            if word == "KPF":
                words.remove(word)
        for w in words:
            w.split()


class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        return True


Abbr = {
    "Air Terminals": "AirTerminals",
    "Cable Tray Fittings": "CableTrayFittings",
    "Cable Tray Runs": "CableTrayRuns",
    "Cable Trays": "CableTrays",
    "Casework": "Cswk",
    "Columns": "Col",
    "Communication Devices": "CommunicationDevices",
    "Conduit Fittings": "ConduitFittings",
    "Conduit Runs": "ConduitRuns",
    "Conduits": "Conduits",
    "Curtain Grids": "CurtainGrids",
    "Curtain Panels": "CurtainPanels",
    "Curtain Systems": "CurtainSystems",
    "Curtain Wall Mullions": "CurtainWallMullions",
    "Data Devices": "DataDevices",
    "Doors": "Door",
    "Duct Accessories": "DuctAccessories",
    "Duct Fittings": "DuctFittings",
    "Duct Insulations": "DuctInsulations",
    "Duct Linings": "DuctLinings",
    "Duct Placeholders": "DuctPlaceholders",
    "Duct Systems": "DuctSystems",
    "Ducts": "Ducts",
    "Electrical Circuits": "ElectricalCircuits",
    "Electrical Equipment": "ElectricalEquipment",
    "Electrical Fixtures": "EleFix",
    "Electrical Spare/Space Circuits": "ElectricalSpare/SpaceCircuits",
    "Entourage": "Entourage",
    "Fire Alarm Devices": "FireAlarmDevices",
    "Flex Ducts": "FlexDucts",
    "Flex Pipes": "FlexPipes",
    "Floors": "Floors",
    "Furniture": "Furn",
    "Furniture Systems": "Furn",
    "Generic Models": "Gm",
    "Generic Annotations": "Ga",
    "HVAC Zones": "HVACZones",
    "Lighting Devices": "LightingDevices",
    "Lighting Fixtures": "Light",
    "Mass": "Mass",
    "Mechanical Equipment": "MechanicalEquipment",
    "Mechanical Equipment Set Boundary Lines": "MechanicalEquipmentSetBoundaryLines",
    "Mechanical Equipment Sets": "MechanicalEquipmentSets",
    "MEP Fabrication Containment": "MEPFabricationContainment",
    "MEP Fabrication Ductwork": "MEPFabricationDuctwork",
    "MEP Fabrication Hangers": "MEPFabricationHangers",
    "MEP Fabrication Pipework": "MEPFabricationPipework",
    "Nurse Call Devices": "NurseCallDevices",
    "Pipe Fittings": "PipeFittings",
    "Pipe Insulations": "PipeInsulations",
    "Pipe Placeholders": "PipePlaceholders",
    "Pipe Segments": "PipeSegments",
    "Pipes": "Pipes",
    "Piping Systems": "PipingSystems",
    "Planting": "Planting",
    "Plumbing Fixtures": "PlumbingFixtures",
    "Security Devices": "SecurityDevices",
    "Site": "Site",
    "Specialty Equipment": "Se",
    "Sprinklers": "Sprinklers",
    "Telephone Devices": "TelephoneDevices",
    "Topography": "Topography",
    "Windows": "Wdw",
    "Railings": "Railings",
    "Structural": "Structural",
    "Supports": "Supports",
    "Terminations": "Terminations",
    "Detail Items": "Detail Items",
    "Profiles": "Profiles",
    "Balusters": "Balusters"
}

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
hosting = {0: "",
            1: "Wl",
            2: "FL",
            3: "CL",
            4: "RF",
            5: "FA"
                    }
specExceptions = ["Railings", "Structural", "Supports", "Terminations"]

material = {"03": ["CONCRETE"],
            "05": ["METALS", "STEEL", "ALUM", "ALUMINIUM", "STL"],
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
        if isfile(join(root, name)) and name[-3:] == "rfa":
            onlyfiles[name[0: -4]] = (str(os.path.join(root, name)))
    for name in directories:

        if isfile(join(root, name)) and name[-3:] == "rfa":
            onlyfiles[name[0: -4]] = (str(os.path.join(root, name)))

# print(onlyfiles)

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, 'Test')
t.Start()
c = 0
with forms.ProgressBar(title='Loading Families(Step 1 of 2)') as pb:
    for i in onlyfiles.values():
        doc.LoadFamily(i, FamilyOption())
        pb.update_progress(c, len(onlyfiles.values()))
        c += 1
t.Commit()

hosts = {}
families = {}
familySymbols = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
for s in familySymbols:
    if s.FamilyName in onlyfiles.keys():
        families[s.FamilyName] = s.Family
        host = s.Family.get_Parameter(BuiltInParameter.FAMILY_HOSTING_BEHAVIOR).AsInteger()
        print(s.FamilyName)
        print(host)
        if host:
            hosts[s.FamilyName] = hosting[host]
        else:
            hosts[s.FamilyName] = ""

famNames = []
# print(families)
count = 0
with forms.ProgressBar(title='Processing Families(Step 2 of 2)') as pb:
    for familyName in families.keys():
        specNumber = "00"
        family = families[familyName]
        cate = family.FamilyCategory.Name
        familyRegex = re.compile(r'\d\d-\S+.*\s?-\s?\S+.*?')
        if len(familyName.split("-")) >= 3 and \
                familyRegex.findall(familyName) >= 1 and \
                cate.upper() == familyName.split("-")[1].upper():

            src_fpath = onlyfiles[familyName]
            dest_fpath = onlyfiles[familyName].replace(folderPath, destinationFolderPath)

            try:
                shutil.copy(src_fpath, dest_fpath)
            except IOError as io_err:
                os.makedirs(os.path.dirname(dest_fpath))
                shutil.copy(src_fpath, dest_fpath)
        else:
            if not "Railings" in cate and not "Structural" in cate and not "Supports" in cate and not "Terminations" in cate:
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

            keywordstoRemove = ["KPF", "_", "-", "Family", "With", ".0001", family.FamilyCategory.Name.ToString()]
            keywordstoRemove.extend(Abbr.keys())
            keywordstoRemove.extend(Abbr.values())
            keywordstoRemove.extend(specSections.keys())

            famHost = hosts[familyName]
            finalName = ""
            if famHost:
                cleanName = (specNumber + "-" + Abbr[family.FamilyCategory.Name.ToString()].title().strip() + "-" +
                             DivideCleanString("-", '_', familyName, keywordstoRemove)).replace(" ", "") + "-" + famHost

            else:
                cleanName = (specNumber + "-" + Abbr[family.FamilyCategory.Name.ToString()].title().strip() + "-" +
                             DivideCleanString("-", '_', familyName, keywordstoRemove)).replace(" ", "")


            print(familyName + ": " + cleanName)

            src_fpath = onlyfiles[familyName]
            dest_fpath = onlyfiles[familyName].replace(folderPath, destinationFolderPath).replace(familyName, cleanName)

            try:
                shutil.copy(src_fpath, dest_fpath)
            except IOError as io_err:
                os.makedirs(os.path.dirname(dest_fpath))
                shutil.copy(src_fpath, dest_fpath)
        pb.update_progress(count, len(families.keys()))
        count += 1
