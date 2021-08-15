
import sys, clr
import ConfigParser
from os.path import expanduser

import Selection
clr.AddReference('System')
from Autodesk.Revit.DB import Document, FilteredElementCollector, Transaction, BuiltInCategory,\
   ElementId, View, ViewSheet

from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

import os
from pyrevit import revit, DB
from pyrevit import forms

#sel_sheets = forms.select_sheets(title='Select Sheets', use_selection=True)

sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
#print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")
#print("Q101" > "Q301")

sheetdic = {}
for sheet in sheets:
    sheetdic[sheet.SheetNumber] = sheet.Title
selSheets = forms. SelectFromList.show(sheets, multiselect=True, name_attr='Title', button_name='Select Sheet')

alert = forms.alert("The operation will overwrite all reference sheet parameter on your sheets, "
            "Please confirm you understand this.")
if alert:
    t = Transaction(doc, 'Fill Reference Parameters')
    t.Start()

    for sheet in selSheets:
        # Reset reference parameter of selected sheets
        try:
            a = 1
            while a < 9:
                sheet.LookupParameter("Reference Sheet " + str(a)).Set("")
                sheet.LookupParameter("Reference Name " + str(a)).Set("")
                a += 1
        except:
            forms.alert("Parameter Error , did not detect enough parameters to fill, "
                        "please check all 1-8 reference parameters are loaded in sheets")
            break


        sheetNumber = sheet.SheetNumber
        #print(sheetNumber)
        sheetReferenceList = {}
        if sheet.SheetNumber != "--":
            views = sheet.GetAllPlacedViews()
            #print("Font Reference")
            for v in views:
                #print(doc.GetElement(v).Title)
                ele = FilteredElementCollector(doc, v).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Viewers).ToElements()
                for e in ele:
                    referenceSheet = e.LookupParameter("Sheet Number").AsString()

                    if referenceSheet != sheetNumber and referenceSheet != "---":
                        sheetReferenceList[referenceSheet] = sheetdic[referenceSheet]
                        #print("Font Reference " + referenceSheet)
                try:
                    backreference = doc.GetElement(v).LookupParameter("Referencing Sheet").AsString()
                    #print("Back Reference " + backreference)
                    if backreference != sheetNumber and backreference != "---" and backreference < sheetNumber:
                        sheetReferenceList[backreference] = sheetdic[backreference]
                        #print("Back Reference " + backreference)
                except:
                    pass
            # print(sheetReferenceList)
            i = 1
            for ss in sheetReferenceList.keys():
                if i < 9:
                    sName = sheetReferenceList[ss].split("-", 1)[1]
                    sheet.LookupParameter("Reference Sheet " + str(i)).Set(ss)
                    sheet.LookupParameter("Reference Name " + str(i)).Set(sName)
                i += 1
                #print(sheet + " " + sName)
    t.Commit()

else:
    alert = forms.alert("Canceled")




