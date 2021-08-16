import clr,sys
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
import System
from Autodesk.Revit.DB import Document
from Autodesk.Revit.UI import RevitCommandId, Events, TaskDialog
from pyrevit import DB, UI
from pyrevit.coreutils import envvars

class CommandReplacement:

    def __init__(self, app, id, replacement):
        #self.uiapp = None
        self.uiControlApp = app
        self.ImportCadWarning = None
        self.importBinding = None
        self.handler = None
        self.id = id
        self.Module_Startup(replacement)

    def Module_Startup(self, replacement):
        if self.uiControlApp != None:
            commandId = RevitCommandId.LookupCommandId(self.id)
            try:
                self.importBinding = self.uiControlApp.CreateAddInCommandBinding(commandId)
                self.handler = System.EventHandler[Events.BeforeExecutedEventArgs](replacement)
                self.importBinding.BeforeExecuted += self.handler
            except:
                TaskDialog.Show("Error", "Mint tool initialization Fail!")

class WarningConstructor:

    def __init__(self, app):
        #self.uiapp = None
        self.Name = None
        self.Title = None
        self.MainMessage = None
        self.MainText = None
        self.ExpandedText = None
        self.VerificationText = None
        self.Link1Text = None
        self.Link2Text = None
        self.Link3Text = None

def ImportWarningWindow():
    ImportCadWarning = TaskDialog("Import CAD Warning")
    ImportCadWarning.MainIcon = UI.TaskDialogIcon.TaskDialogIconWarning
    ImportCadWarning.Title = "Import CAD Warning"
    ImportCadWarning.TitleAutoPrefix = True
    ImportCadWarning.AllowCancellation = False

    ImportCadWarning.MainInstruction = "Import CAD is strongly NOT recommended by KPF Digital Practice. Please use Link CAD instead."
    ImportCadWarning.ExpandedContent = None
    #ImportCadWarning.ExpandedContent = "This is 'ExpandedContent'.\nLine1: blar blar...\nLine2: blar blar...\nLine3: blar blar...";

    #ImportCadWarning.VerificationText = "This is 'VerificationText'."

    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink1, "Yes, I want to use Link CAD instead.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink2, "Ok, Cancel this for me.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink3, "No, I still want to proceed.")

    ImportCadWarning.CommonButtons = UI.TaskDialogCommonButtons.None
    return ImportCadWarning

def ImportReplacement(sender, args):
    if args.ActiveDocument.IsFamilyDocument:
        args.Cancel = False
    else:
        result = ImportWarningWindow().Show()
        if result == UI.TaskDialogResult.CommandLink1:
            __revit__.PostCommand(RevitCommandId.LookupPostableCommandId(UI.PostableCommand.LinkCAD))
            args.Cancel = True
        elif result == result == UI.TaskDialogResult.CommandLink2:
            args.Cancel = True
        elif result == UI.TaskDialogResult.CommandLink3:
            args.Cancel = False

def WallOpeningWindow():
    ImportCadWarning = TaskDialog("Wall Opening Warning")
    ImportCadWarning.MainIcon = UI.TaskDialogIcon.TaskDialogIconWarning
    ImportCadWarning.Title = "Wall Opening Warning"
    ImportCadWarning.TitleAutoPrefix = True
    ImportCadWarning.AllowCancellation = False

    ImportCadWarning.MainInstruction = "Wall Opening is strongly NOT recommended by KPF Digital Practice. Please use wall opening family."
    ImportCadWarning.ExpandedContent = None
    #ImportCadWarning.ExpandedContent = "This is 'ExpandedContent'.\nLine1: blar blar...\nLine2: blar blar...\nLine3: blar blar...";

    #ImportCadWarning.VerificationText = "This is 'VerificationText'."

    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink1,
                                    "Yes, I want to use wall opening family instead.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink2, "Ok, Cancel this for me.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink3, "No, I still want to proceed.")

    ImportCadWarning.CommonButtons = UI.TaskDialogCommonButtons.None
    return ImportCadWarning


def WallOpeningReplacement(sender, args):
    # TODO: Get the wall opening family/ load the family if it is not found
    wallOpeningFam = None
    if args.ActiveDocument.IsFamilyDocument:
        args.Cancel = False
    else:
        result = ImportWarningWindow().Show()
        if result == UI.TaskDialogResult.CommandLink1:
            __revit__.ActiveUIDocument.PromptForFamilyInstancePlacement(wallOpeningFam)
            args.Cancel = True
        elif result == result == UI.TaskDialogResult.CommandLink2:
            args.Cancel = True
        elif result == UI.TaskDialogResult.CommandLink3:
            args.Cancel = False