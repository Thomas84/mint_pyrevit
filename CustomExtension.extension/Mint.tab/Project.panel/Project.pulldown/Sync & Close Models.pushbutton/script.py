import sys, clr, os, re
import ConfigParser
from os.path import expanduser
from Autodesk.Revit.DB import Document, SynchronizeWithCentralOptions, TransactWithCentralOptions, RelinquishOptions
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__doc__ = 'Syncs background documents and close the document.' \
          'Does not work on the currently active model.'

activeDocuments = doc.Application.Documents
syncOption = SynchronizeWithCentralOptions()
transOption = TransactWithCentralOptions()
relinquishOption = RelinquishOptions(True)
syncOption.SetRelinquishOptions(relinquishOption)

nameLst = []
for document in activeDocuments:
    if not document.IsLinked  and document != doc:
        nameLst.append(document.Title)
if len(nameLst) > 0:
    selDocs = forms.SelectFromList.show(nameLst, multiselect=True, button_name='Select Documents')
    for document in activeDocuments:
        try:
            if document.Title in selDocs and not document.IsLinked  and document != doc:
                document.SynchronizeWithCentral(transOption, syncOption)
                if document.Title == uidoc.Document.Title:
                    pass
                else:
                    document.Close()
        except:
            pass



else:
    print("Did not detect active document")
