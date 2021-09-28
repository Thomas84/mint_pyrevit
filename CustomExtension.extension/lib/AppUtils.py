import System.Diagnostics
import sys, clr, os, re
from Autodesk.Revit.DB import Document, SynchronizeWithCentralOptions, TransactWithCentralOptions, RelinquishOptions
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

def ShutdownApp():
    process = System.Diagnostics.Process.GetCurrentProcess()
    print(process)
    process.Kill()

def SyncSaveandCloseModels(uidoc):
    activeDocuments = uidoc.Application.Documents
    syncOption = SynchronizeWithCentralOptions()
    syncOption.SaveLocalBefore = True
    transOption = TransactWithCentralOptions()
    relinquishOption = RelinquishOptions(True)
    syncOption.SetRelinquishOptions(relinquishOption)

    if activeDocuments:
        for document in activeDocuments:
            if not document.IsLinked:
                # document.Save()
                document.SynchronizeWithCentral(transOption, syncOption)
                if document != uidoc.Document:
                    document.Close()
                else:
                    pass
            else:
                document.Save()
        ShutdownApp()
    else:
        ShutdownApp()
