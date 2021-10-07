import System
import sys, clr, os, re
import ConfigParser
from os.path import expanduser
# Set system path
from Autodesk.Revit.DB import Document, SynchronizeWithCentralOptions, TransactWithCentralOptions, RelinquishOptions
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')


def SyncandCloseRevit(uiapp, home):
    activeDocuments = uiapp.Application.Documents
    syncOption = SynchronizeWithCentralOptions()
    transOption = TransactWithCentralOptions()
    relinquishOption = RelinquishOptions(True)
    syncOption.SetRelinquishOptions(relinquishOption)
    syncOption.SaveLocalBefore = True
    syncOption.Comment = "idleAutoSync"

    for document in activeDocuments:
        if not document.IsFamilyDocument and not document.IsLinked:
            document.SynchronizeWithCentral(transOption, syncOption)
            if not document.Title == uiapp.ActiveUIDocument.Document.Title:
                document.Close()
        elif not document.IsLinked:
            if document.PathName:
                document.Save()
            else:
                document.SaveAs(home + "\\" + document.Title + ".rfa")
            if not document.Title == uiapp.ActiveUIDocument.Document.Title:
                document.Close()
        else:
            pass
    process = System.Diagnostics.Process.GetCurrentProcess()
    process.Kill()
