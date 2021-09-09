
import sys, clr, os, re
import ConfigParser
from os.path import expanduser
# Set system path


from Autodesk.Revit.DB import Document, SynchronizeWithCentralOptions, TransactWithCentralOptions, RelinquishOptions
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Pick the files you want to sync and close.'

activeDocuments = doc.Application.Documents
syncOption = SynchronizeWithCentralOptions()
transOption = TransactWithCentralOptions()
relinquishOption = RelinquishOptions(True)
syncOption.SetRelinquishOptions(relinquishOption)

nameLst = []
for document in activeDocuments:
    nameLst.append(document.Title)

selDocs = forms.SelectFromList.show(nameLst, multiselect=True, button_name='Select Documents')
for document in activeDocuments:
    if document.Title in selDocs:

        document.SynchronizeWithCentral(transOption, syncOption)
        if document.Title == uidoc.Document.Title:
            pass
        else:
            document.Close()

