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
            commandId = RevitCommandId.LookupPostableCommandId(self.id)
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

    ImportCadWarning.MainInstruction = "Import CAD is strongly discouraged by KPF Digital Practice. Please use Link CAD instead."
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
def ModelInPlaceWindow():
    ImportCadWarning = TaskDialog("Model-In-PlaceWarning")
    ImportCadWarning.MainIcon = UI.TaskDialogIcon.TaskDialogIconWarning
    ImportCadWarning.Title = "Model-In-Place Warning"
    ImportCadWarning.TitleAutoPrefix = True
    ImportCadWarning.AllowCancellation = False

    ImportCadWarning.MainInstruction = "Model-In-Place is strongly discouraged by KPF Digital Practice. Please create a Family Instead."
    ImportCadWarning.ExpandedContent = None
    #ImportCadWarning.ExpandedContent = "This is 'ExpandedContent'.\nLine1: blar blar...\nLine2: blar blar...\nLine3: blar blar...";

    #ImportCadWarning.VerificationText = "This is 'VerificationText'."

    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink1, "Yes, Cancel this for me.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink2, "Ok, I want to learn about building Family.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink3, "No, I still want to proceed.")

    ImportCadWarning.CommonButtons = UI.TaskDialogCommonButtons.None
    return ImportCadWarning

def ModelInPlaceReplacement(sender, args):
    if args.ActiveDocument.IsFamilyDocument:
        args.Cancel = False
    else:
        result = ModelInPlaceWindow().Show()
        if result == UI.TaskDialogResult.CommandLink1:
            args.Cancel = True
        elif result == result == UI.TaskDialogResult.CommandLink2:
            System.Diagnostics.Process.Start("https://portal.pinnacleseries.com/#/learningcenter/series?learningPathId=2bc9e249-69bc-40b0-8946-f8326a159a0b");
            args.Cancel = True
        elif result == UI.TaskDialogResult.CommandLink3:
            args.Cancel = False
def WallOpeningWindow():
    ImportCadWarning = TaskDialog("Wall Opening Warning")
    ImportCadWarning.MainIcon = UI.TaskDialogIcon.TaskDialogIconWarning
    ImportCadWarning.Title = "Wall Opening Warning"
    ImportCadWarning.TitleAutoPrefix = True
    ImportCadWarning.AllowCancellation = False

    ImportCadWarning.MainInstruction = "Wall Opening is strongly discouraged by KPF Digital Practice. Please use wall opening family."
    ImportCadWarning.ExpandedContent = None
    #ImportCadWarning.ExpandedContent = "This is 'ExpandedContent'.\nLine1: blar blar...\nLine2: blar blar...\nLine3: blar blar...";

    #ImportCadWarning.VerificationText = "This is 'VerificationText'."

    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink1,
                                    "Yes, I want to use wall opening family instead.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink2, "Ok, Cancel this for me.")
    ImportCadWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink3, "No, I still want to proceed.")

    ImportCadWarning.CommonButtons = UI.TaskDialogCommonButtons.None
    return ImportCadWarning

class FamilyOption(DB.IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True

	def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		return True

def GetFamily(doc, name, path):
    fam = None
    FSymbol = DB.FilteredElementCollector(doc) \
        .OfClass(clr.GetClrType(DB.FamilySymbol)) \
        .ToElements()
    for i in FSymbol:
        if i.Family.Name == name:
            fam = i
            t = DB.Transaction(doc, 'Test')
            t.Start()
            if not fam.IsActive:
                fam.Activate()
                doc.Regenerate()
            t.Commit()
            return fam
    if fam is None:
        t = DB.Transaction(doc, 'Test')
        t.Start()
        wallOpeningFam = doc.LoadFamily(
            path, FamilyOption())
        fam = wallOpeningFam[1]
        symbol = doc.GetElement(list(fam.GetFamilySymbolIds())[0])
        symbol.Activate()
        doc.Regenerate()
        t.Commit()

        return symbol

class PlaceWallOpeningEventHandler(UI.IExternalEventHandler):
    name = 'MyCustomExternalEventHandler'

    def Execute(self, uiapp):
        wallOpeningFam = GetFamily(uiapp.ActiveUIDocument.Document, 'Wall Opening_DD',
                    '\\\\kpf.com\\corporate\\Zdrive\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa')
        uiapp.ActiveUIDocument.PostRequestForElementTypePlacement(wallOpeningFam)

    def GetName(self):
        """String identification of the event handler."""
        return self.name

def WallOpeningReplacement(sender, args):
    # TODO: Get the wall opening family/ load the family if it is not found
    #wallOpeningFam = GetFamily(__revit__.ActiveUIDocument, 'Wall Opening_DD', r'Z:\0002_03_BIM\03_Workflows\KPFTools\Family\Wall Opening_DD.rfa')
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    if args.ActiveDocument.IsFamilyDocument:
        args.Cancel = False
    else:
        result = WallOpeningWindow().Show()
        if result == UI.TaskDialogResult.CommandLink1:
            args.Cancel = True
            extevent_hndlr = PlaceWallOpeningEventHandler()
            extevent = UI.ExternalEvent.Create(extevent_hndlr)
            extevent.Raise()
            #wallOpeningFam = GetFamily(doc, 'Wall Opening_DD', 'Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa')
            #uidoc.PostRequestForElementTypePlacement(wallOpeningFam)

        elif result == result == UI.TaskDialogResult.CommandLink2:
            args.Cancel = True
        elif result == UI.TaskDialogResult.CommandLink3:
            args.Cancel = False