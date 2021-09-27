import clr
from pyrevit import DB, UI, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Gets all sheets number, name, index in model and linked models.'
__author__ = 'Mengfan Lou'

activeDocuments = doc.Application.Documents

docLst = []
for document in activeDocuments:
    docLst.append(document)


for d in docLst:
    sheets = DB.FilteredElementCollector(d).OfClass(DB.ViewSheet).ToElements()
    for sheet in sheets:
        index = ""
        try:
            index = str(sheet.LookupParameter("SHEET ORDER INDEX").AsDouble())
        except:
            index = ""
        print(d.Title + " " + sheet.SheetNumber + "-" + sheet.Title + " index: " + index)
